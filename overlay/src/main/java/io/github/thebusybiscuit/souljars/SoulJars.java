package io.github.thebusybiscuit.souljars;

import io.github.thebusybiscuit.slimefun4.api.SlimefunAddon;
import io.github.thebusybiscuit.slimefun4.api.items.ItemGroup;
import io.github.thebusybiscuit.slimefun4.api.items.SlimefunItem;
import io.github.thebusybiscuit.slimefun4.api.items.SlimefunItemStack;
import io.github.thebusybiscuit.slimefun4.api.recipes.RecipeType;
import io.github.thebusybiscuit.slimefun4.implementation.SlimefunItems;
import io.github.thebusybiscuit.slimefun4.implementation.items.blocks.BrokenSpawner;
import io.github.thebusybiscuit.slimefun4.implementation.items.blocks.UnplaceableBlock;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.EntityType;
import org.bukkit.event.Listener;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.configuration.file.YamlConfiguration;
import io.github.thebusybiscuit.slimefun4.implementation.Slimefun;
import com.wickidcow.slimefununified.runtime.UnifiedRuntime;
import java.nio.file.Path;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.charset.StandardCharsets;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.logging.Logger;
import org.bukkit.Server;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.logging.Level;

/**
 * Adapted from TheBusyBiscuit SoulJars (GPLv3), source pinned in the
 * SlimefunUnified integration manifest. Original item and gameplay logic
 * retained; only the standalone JavaPlugin bootstrap is replaced here.
 */
public class SoulJars implements Listener, SlimefunAddon {
    private static SoulJars instance;
    private final Slimefun core;
    private final Path configPath;
    private final YamlConfiguration config;

    private SoulJars(Slimefun core, Path configPath, YamlConfiguration config) {
        this.core = core;
        this.configPath = configPath;
        this.config = config;
    }

    public static void start(Slimefun core) {
        if (core.getServer().getPluginManager().getPlugin("SoulJars") != null) {
            core.getLogger().warning("Standalone SoulJars detected; Unified SoulJars module skipped to prevent duplicate item registrations.");
            return;
        }
        try {
            Path path = new File(core.getDataFolder().getParentFile(), "SoulJars/config.yml").toPath();
            if (!Files.isRegularFile(path)) {
                Files.createDirectories(path.getParent());
                try (InputStream source = core.getResource("unified/addons/souljars/config.yml")) {
                    if (source == null) throw new IOException("No bundled original SoulJars default config");
                    Files.copy(source, path);
                }
            }
            YamlConfiguration config = new YamlConfiguration();
            config.load(path.toFile());
            SoulJars module = new SoulJars(core, path, config);
            instance = module;
            module.initializeItems();
            UnifiedRuntime.registerBundledAddon("souljars", module);
            core.getLogger().info("SlimefunUnified: initialized SoulJars module; existing configs retained");
        } catch (IOException | org.bukkit.configuration.InvalidConfigurationException | IllegalArgumentException exception) {
            instance = null;
            core.getLogger().log(Level.SEVERE, "Failed to initialize embedded SoulJars; saved data was not deleted", exception);
        }
    }

    public Logger getLogger() {
        return core.getLogger();
    }

    public Server getServer() {
        return core.getServer();
    }

    public FileConfiguration getConfig() {
        return config;
    }

    public void saveConfig() {
        try {
            Files.createDirectories(configPath.getParent());
            Path temp = Files.createTempFile(configPath.getParent(), "souljars-", ".tmp");
            try {
                Files.writeString(temp, config.saveToString(), StandardCharsets.UTF_8);
                try {
                    Files.move(temp, configPath, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
                } catch (AtomicMoveNotSupportedException ignored) {
                    Files.move(temp, configPath, StandardCopyOption.REPLACE_EXISTING);
                }
            } finally {
                Files.deleteIfExists(temp);
            }
        } catch (IOException exception) {
            core.getLogger().log(Level.SEVERE, "Could not save historical SoulJars configuration", exception);
        }
    }


    private static final String JAR_TEXTURE = "bd1c777ee166c47cae698ae6b769da4e2b67f468855330ad7bddd751c5293f";
    private final Map<EntityType, Integer> mobs = new HashMap<>();

    private ItemGroup itemGroup;
    private RecipeType recipeType;
    private SlimefunItemStack emptyJar;

    private void initializeItems() {

        emptyJar = new SlimefunItemStack(
            "SOUL_JAR",
            JAR_TEXTURE,
            "&bSoul Jar &7(Empty)",
            "",
            "&rKill a mob while carrying this",
            "&rin your inventory to bind its soul."
        );

        ItemStack categoryIcon = emptyJar.clone();
        setNameAndLore(categoryIcon, "&bSoul Jars", "", "&a> Click to open");
        itemGroup = new ItemGroup(java.util.Objects.requireNonNull(NamespacedKey.fromString("souljars:soul_jars")), categoryIcon);

        ItemStack recipeIcon = new ItemStack(Material.DIAMOND_SWORD);
        setNameAndLore(recipeIcon, "&cKill the specified mob", "&cwhile carrying an empty Soul Jar");
        recipeType = new RecipeType(java.util.Objects.requireNonNull(NamespacedKey.fromString("souljars:mob_killing")), recipeIcon);

        ItemStack output = emptyJar.clone();
        output.setAmount(3);
        new SlimefunItem(
            itemGroup,
            emptyJar,
            RecipeType.ANCIENT_ALTAR,
            new ItemStack[] {
                SlimefunItems.EARTH_RUNE, new ItemStack(Material.SOUL_SAND), SlimefunItems.WATER_RUNE,
                new ItemStack(Material.SOUL_SAND), SlimefunItems.NECROTIC_SKULL, new ItemStack(Material.SOUL_SAND),
                SlimefunItems.AIR_RUNE, new ItemStack(Material.SOUL_SAND), SlimefunItems.FIRE_RUNE
            },
            output
        ).register(this);

        new JarsListener(this);
        registerConfiguredMobs();
        saveConfig();
    }

    private void registerConfiguredMobs() {
        FileConfiguration config = getConfig();
        Set<String> configured = new LinkedHashSet<>(config.getStringList("mobs"));
        if (config.getBoolean("options.include-modern-mobs", true)) {
            configured.addAll(config.getStringList("modern-mobs"));
        }

        for (String mobName : configured) {
            EntityType type = resolveEntityType(mobName);
            if (type == null) {
                getLogger().log(Level.WARNING, "Skipping invalid mob type from config: {0}", mobName);
                continue;
            }
            if (mobs.containsKey(type)) {
                continue;
            }
            registerSoul(type);
        }
    }

    /** Retains historical item IDs where modern Paper changes EntityType field names. */
    public static String legacyEntityId(EntityType type) {
        String name = type.getKey().getKey().toUpperCase(Locale.ROOT);
        return "MOOSHROOM".equals(name) ? "MUSHROOM_COW" : name;
    }

    private EntityType resolveEntityType(String configuredName) {
        if (configuredName == null || configuredName.isBlank()) {
            return null;
        }

        String normalized = configuredName.trim().toUpperCase(Locale.ROOT).replace('-', '_').replace(' ', '_');
        // Preserve older working configs that used Bukkit's historical Pig Zombie name.
        if (normalized.equals("PIG_ZOMBIE")) {
            normalized = "ZOMBIFIED_PIGLIN";
        }

        if (normalized.equals("MUSHROOM_COW")) normalized = "MOOSHROOM";
        try {
            // Modern Paper versions no longer represent EntityType as an enum.
            Object resolved = EntityType.class.getField(normalized).get(null);
            return resolved instanceof EntityType found ? found : null;
        } catch (ReflectiveOperationException ex) {
            return null;
        }
    }

    private void registerSoul(EntityType type) {
        String name = humanize(legacyEntityId(type));
        String path = "souls-required." + legacyEntityId(type);
        FileConfiguration config = getConfig();
        int souls = config.isInt(path) ? Math.max(1, config.getInt(path)) : 128;
        if (!config.isInt(path)) {
            config.set(path, souls);
        }
        mobs.put(type, souls);

        Material mobEgg = Material.getMaterial(legacyEntityId(type) + "_SPAWN_EGG");
        if (mobEgg == null) {
            mobEgg = Material.ZOMBIE_SPAWN_EGG;
        }

        SlimefunItemStack jarItem = new SlimefunItemStack(
            legacyEntityId(type) + "_SOUL_JAR",
            JAR_TEXTURE,
            "&cSoul Jar &7(" + name + ")",
            "",
            "&7Infused Souls: &e1"
        );
        ItemStack killIcon = new ItemStack(mobEgg);
        setNameAndLore(killIcon, "&rKill " + souls + "x " + name);
        new UnplaceableBlock(
            itemGroup,
            jarItem,
            recipeType,
            new ItemStack[] { null, null, null, emptyJar, null, killIcon, null, null, null }
        ).register(this);

        SlimefunItemStack filledJarItem = new SlimefunItemStack(
            "FILLED_" + legacyEntityId(type) + "_SOUL_JAR",
            JAR_TEXTURE,
            "&cFilled Soul Jar &7(" + name + ")",
            "",
            "&7Infused Souls: &e" + souls
        );
        new FilledJar(
            itemGroup,
            filledJarItem,
            recipeType,
            new ItemStack[] { null, null, null, emptyJar, null, killIcon, null, null, null }
        ).register(this);

        BrokenSpawner brokenSpawner = SlimefunItems.BROKEN_SPAWNER.getItem(BrokenSpawner.class);
        SlimefunItemStack spawnerItem = new SlimefunItemStack(
            legacyEntityId(type) + "_BROKEN_SPAWNER",
            Material.SPAWNER,
            "&cBroken Spawner &7(" + name + ")"
        );
        new SlimefunItem(
            itemGroup,
            spawnerItem,
            RecipeType.ANCIENT_ALTAR,
            new ItemStack[] {
                new ItemStack(Material.IRON_BARS), SlimefunItems.EARTH_RUNE, new ItemStack(Material.IRON_BARS),
                SlimefunItems.EARTH_RUNE, filledJarItem, SlimefunItems.EARTH_RUNE,
                new ItemStack(Material.IRON_BARS), SlimefunItems.EARTH_RUNE, new ItemStack(Material.IRON_BARS)
            },
            brokenSpawner.getItemForEntityType(type)
        ).register(this);
    }

    private static String humanize(String enumName) {
        String[] parts = enumName.toLowerCase(Locale.ROOT).split("_");
        StringBuilder result = new StringBuilder();
        for (String part : parts) {
            if (!result.isEmpty()) {
                result.append(' ');
            }
            result.append(Character.toUpperCase(part.charAt(0))).append(part.substring(1));
        }
        return result.toString();
    }

    private static void setNameAndLore(ItemStack item, String name, String... lore) {
        ItemMeta meta = item.getItemMeta();
        if (meta == null) {
            return;
        }
        meta.setDisplayName(color(name));
        List<String> lines = new ArrayList<>(lore.length);
        for (String line : lore) {
            lines.add(color(line));
        }
        meta.setLore(lines);
        item.setItemMeta(meta);
    }

    private static String color(String text) {
        return ChatColor.translateAlternateColorCodes('&', text);
    }

    public Map<EntityType, Integer> getRequiredSouls() {
        return mobs;
    }

    @Override
    public JavaPlugin getJavaPlugin() {
        return core;
    }

    @Override
    public String getName() {
        return "SoulJars";
    }

    @Override
    public String getBugTrackerURL() {
        return "https://github.com/wickidcow/SF_SoulJars/issues";
    }
}
