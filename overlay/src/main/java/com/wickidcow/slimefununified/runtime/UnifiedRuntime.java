package com.wickidcow.slimefununified.runtime;

import com.wickidcow.slimefununified.policy.AddonModule;
import com.wickidcow.slimefununified.policy.ModuleCatalog;
import com.wickidcow.slimefununified.policy.PolicyRules;
import io.github.thebusybiscuit.slimefun4.api.SlimefunAddon;
import io.github.thebusybiscuit.slimefun4.api.items.SlimefunItem;
import io.github.thebusybiscuit.slimefun4.implementation.Slimefun;
import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Locale;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.logging.Level;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.InvalidConfigurationException;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

/**
 * One source of truth for Unified-specific player Guide and manual crafting rules.
 * Hidden items are NEVER unregistered, removed, migrated or made invalid.
 *
 * This prototype bundles core only. Additional addon ownership must be explicitly bound
 * during future integration; unknown external items are never guessed from their ID.
 */
public final class UnifiedRuntime {
    private static final String FILE_NAME = "UnifiedModules.yml";
    private static final String PERMISSION = "slimefununified.admin";
    private static volatile UnifiedRuntime runtime;

    private final Slimefun plugin;
    private final File configFile;
    private final ConcurrentMap<String, String> itemOwners = new ConcurrentHashMap<>();
    private final ConcurrentMap<SlimefunAddon, String> addonOwners = new ConcurrentHashMap<>();
    private final Set<String> bundled = ConcurrentHashMap.newKeySet();
    private volatile PolicyRules rules;
    private volatile YamlConfiguration config;
    private volatile boolean writable;

    private UnifiedRuntime(Slimefun plugin) {
        this.plugin = plugin;
        this.configFile = new File(plugin.getDataFolder(), FILE_NAME);
        bundled.add("slimefun");
        this.rules = defaultPolicy();
        this.config = defaults();
        this.writable = false;
        readConfig();
    }

    public static synchronized void initialize(Slimefun plugin) {
        if (runtime == null) {
            runtime = new UnifiedRuntime(plugin);
        }
    }

    public static boolean isOwner(Player player) {
        return player != null && player.hasPermission(PERMISSION);
    }

    public static boolean isBundled(String moduleId) {
        UnifiedRuntime current = runtime;
        return current != null && current.bundled.contains(moduleId);
    }

    /**
     * Binds a distinct embedded SlimefunAddon facade rather than the shared JavaPlugin.
     * This covers both existing and subsequently registered item IDs.
     */
    public static void registerBundledAddon(String moduleId, SlimefunAddon addon) {
        UnifiedRuntime current = runtime;
        if (current == null) throw new IllegalStateException("Unified has not initialized");
        boolean known = ModuleCatalog.candidates().stream().anyMatch(m -> moduleId.equals(m.id()));
        if (!known || "slimefun".equals(moduleId) || addon == null) {
            throw new IllegalArgumentException("Invalid bundled addon identity: " + moduleId);
        }
        String existing = current.addonOwners.putIfAbsent(addon, moduleId);
        if (existing != null && !existing.equals(moduleId)) {
            throw new IllegalArgumentException("Addon identity already owned by " + existing);
        }
        current.bundled.add(moduleId);
    }

    /** Future integrated modules call this only after their own item registration. */
    public static void registerBundledModule(String moduleId, Iterable<String> itemIds) {
        UnifiedRuntime current = runtime;
        if (current == null) throw new IllegalStateException("Unified has not initialized");
        boolean known = ModuleCatalog.candidates().stream().map(AddonModule::id).anyMatch(moduleId::equals);
        if (!known || "slimefun".equals(moduleId)) {
            throw new IllegalArgumentException("Invalid addon module: " + moduleId);
        }
        for (String id : itemIds) {
            if (SlimefunItem.getById(id) == null) {
                throw new IllegalArgumentException("Cannot bind unregistered Slimefun item: " + id);
            }
            String previous = current.itemOwners.putIfAbsent(id.toUpperCase(Locale.ROOT), moduleId);
            if (previous != null && !previous.equals(moduleId)) {
                throw new IllegalArgumentException("Conflicting item owner: " + id);
            }
        }
        current.bundled.add(moduleId);
    }

    public static boolean isVisible(Player player, SlimefunItem item) {
        UnifiedRuntime current = runtime;
        if (current == null || player == null || item == null) return true;
        String owner = current.findOwner(item);
        if (owner == null) return true;
        return current.rules.guideVisible(owner, item.getId(), actor(player)).allowed();
    }

    public static boolean denyPlayerCraft(Player player, ItemStack output) {
        UnifiedRuntime current = runtime;
        if (current == null || player == null || output == null) return false;
        SlimefunItem item = SlimefunItem.getByItem(output);
        if (item == null) return false;
        String owner = current.findOwner(item);
        if (owner == null) return false;
        PolicyRules.Decision decision = current.rules.manualCraftingAllowed(owner, item.getId(), actor(player));
        if (decision.allowed()) return false;
        player.sendMessage("§cPlayer crafting is disabled for " + item.getItemName()
                + " §7(" + item.getId() + ")");
        return true;
    }

    public static boolean guideVisibleFlag(String moduleId) {
        UnifiedRuntime current = runtime;
        return current == null || current.config.getBoolean("modules." + moduleId + ".guide-visible", true);
    }

    public static boolean craftingFlag(String moduleId) {
        UnifiedRuntime current = runtime;
        return current == null || current.config.getBoolean("modules." + moduleId + ".player-crafting", true);
    }

    public static boolean writable() {
        UnifiedRuntime current = runtime;
        return current != null && current.writable;
    }

    /** All mutators require OP permission, an actual bundled module, and an atomic save. */
    public static boolean toggle(Player player, String moduleId, String flag) {
        UnifiedRuntime current = runtime;
        if (!isOwner(player) || current == null || !current.writable || !current.bundled.contains(moduleId)) {
            return false;
        }
        if (!"guide-visible".equals(flag) && !"player-crafting".equals(flag)) {
            return false;
        }
        return current.toggleAndSave(moduleId, flag);
    }

    private synchronized boolean toggleAndSave(String moduleId, String flag) {
        String key = "modules." + moduleId + "." + flag;
        try {
            YamlConfiguration proposed = new YamlConfiguration();
            proposed.loadFromString(config.saveToString());
            proposed.set(key, !proposed.getBoolean(key, true));
            PolicyRules candidate = parsePolicy(proposed);
            saveAtomically(proposed);
            config = proposed;
            rules = candidate;
            plugin.getLogger().info("Unified player policy changed: " + key + "=" + proposed.getBoolean(key));
            return true;
        } catch (IOException | InvalidConfigurationException | IllegalArgumentException exception) {
            plugin.getLogger().log(Level.SEVERE, "Unable to save Unified module policy; old policy remains", exception);
            return false;
        }
    }

    private void readConfig() {
        try {
            YamlConfiguration loaded = defaults();
            if (configFile.isFile()) {
                loaded.load(configFile);
            }
            PolicyRules parsed = parsePolicy(loaded);
            if (!configFile.isFile()) saveAtomically(loaded);
            config = loaded;
            rules = parsed;
            writable = true;
        } catch (IOException | InvalidConfigurationException | IllegalArgumentException exception) {
            plugin.getLogger().log(Level.SEVERE,
                    "Invalid UnifiedModules.yml; preserving existing file and denying non-OP core access", exception);
            config = deniedByDefault();
            rules = failClosedPolicy();
            writable = false;
        }
    }

    private static YamlConfiguration defaults() {
        YamlConfiguration yaml = new YamlConfiguration();
        yaml.set("modules.slimefun.guide-visible", true);
        yaml.set("modules.slimefun.player-crafting", true);
        return yaml;
    }

    private static YamlConfiguration deniedByDefault() {
        YamlConfiguration yaml = new YamlConfiguration();
        for (AddonModule candidate : ModuleCatalog.candidates()) {
            yaml.set("modules." + candidate.id() + ".guide-visible", false);
            yaml.set("modules." + candidate.id() + ".player-crafting", false);
        }
        return yaml;
    }

    private static PolicyRules defaultPolicy() {
        try {
            return parsePolicy(defaults());
        } catch (Exception impossible) {
            throw new IllegalStateException(impossible);
        }
    }

    private static PolicyRules failClosedPolicy() {
        try {
            return parsePolicy(deniedByDefault());
        } catch (Exception impossible) {
            throw new IllegalStateException(impossible);
        }
    }

    private static PolicyRules parsePolicy(YamlConfiguration yaml) throws IOException {
        StringBuilder properties = new StringBuilder();
        extractRules(yaml.getConfigurationSection("modules"), properties, "module", false);
        extractRules(yaml.getConfigurationSection("items"), properties, "item", true);
        if (yaml.contains("modules") && !yaml.isConfigurationSection("modules")
                || yaml.contains("items") && !yaml.isConfigurationSection("items")) {
            throw new IllegalArgumentException("Unified module/items sections must be YAML mappings");
        }
        return PolicyRules.fromProperties(new StringReader(properties.toString()), ModuleCatalog.candidates());
    }

    private static void extractRules(ConfigurationSection root, StringBuilder out, String prefix, boolean items) {
        if (root == null) return;
        for (String moduleId : root.getKeys(false)) {
            ConfigurationSection module = root.getConfigurationSection(moduleId);
            if (module == null) throw new IllegalArgumentException("Expected mapping for " + prefix + "." + moduleId);
            if (items) {
                for (String itemId : module.getKeys(false)) {
                    ConfigurationSection item = module.getConfigurationSection(itemId);
                    if (item == null) throw new IllegalArgumentException("Expected mapping for item " + itemId);
                    appendFlags(out, prefix + "." + moduleId + "." + itemId, item);
                }
            } else {
                appendFlags(out, prefix + "." + moduleId, module);
            }
        }
    }

    private static void appendFlags(StringBuilder out, String key, ConfigurationSection section) {
        for (String flag : section.getKeys(false)) {
            if (!"guide-visible".equals(flag) && !"player-crafting".equals(flag)) {
                throw new IllegalArgumentException("Unknown Unified setting: " + key + "." + flag);
            }
            if (!section.isBoolean(flag)) {
                throw new IllegalArgumentException("Unified setting must be true/false: " + key + "." + flag);
            }
            out.append(key).append('.').append(flag).append('=')
                    .append(section.getBoolean(flag)).append('\n');
        }
    }

    private void saveAtomically(YamlConfiguration yaml) throws IOException {
        Path dest = configFile.toPath();
        Files.createDirectories(dest.getParent());
        Path temp = Files.createTempFile(dest.getParent(), "UnifiedModules-", ".tmp");
        try {
            Files.writeString(temp, yaml.saveToString(), StandardCharsets.UTF_8);
            try {
                Files.move(temp, dest, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
            } catch (AtomicMoveNotSupportedException ignored) {
                Files.move(temp, dest, StandardCopyOption.REPLACE_EXISTING);
            }
        } finally {
            Files.deleteIfExists(temp);
        }
    }

    private String findOwner(SlimefunItem item) {
        String explicit = itemOwners.get(item.getId().toUpperCase(Locale.ROOT));
        if (explicit != null) return explicit;
        String addonOwner = addonOwners.get(item.getAddon());
        if (addonOwner != null) return addonOwner;
        return "Slimefun".equalsIgnoreCase(item.getAddon().getJavaPlugin().getName()) ? "slimefun" : null;
    }

    private static PolicyRules.Actor actor(Player player) {
        return isOwner(player) ? PolicyRules.Actor.OP : PolicyRules.Actor.PLAYER;
    }
}
