package com.wickidcow.slimefununified.policy;

import java.io.IOException;
import java.io.Reader;
import java.util.Collection;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Properties;

/**
 * Policy only. Does not remove items or disable loaded modules.
 * Caller must enforce guide filtering and manual crafting in every supported integration.
 */
public final class PolicyRules {
    public enum Actor { PLAYER, OP, AUTOMATION }

    public record Decision(boolean allowed, String reason) {}
    private record Flags(boolean guideVisible, boolean playerCrafting) {
        private static final Flags DEFAULT = new Flags(true, true);

        private Flags set(String property, boolean state) {
            return switch (property) {
                case "guide-visible" -> new Flags(state, playerCrafting);
                case "player-crafting" -> new Flags(guideVisible, state);
                default -> throw new IllegalArgumentException("Unsupported property: " + property);
            };
        }
    }

    private final Map<String, AddonModule> catalog;
    private final Map<String, Flags> moduleRules;
    private final Map<String, Flags> itemRules;

    private PolicyRules(Map<String, AddonModule> catalog, Map<String, Flags> moduleRules,
                        Map<String, Flags> itemRules) {
        this.catalog = Map.copyOf(catalog);
        this.moduleRules = Map.copyOf(moduleRules);
        this.itemRules = Map.copyOf(itemRules);
    }

    public static PolicyRules fromProperties(Reader reader, Collection<AddonModule> modules) throws IOException {
        Objects.requireNonNull(reader, "reader");
        Objects.requireNonNull(modules, "modules");
        Map<String, AddonModule> catalog = new HashMap<>();
        for (AddonModule module : modules) {
            if (catalog.putIfAbsent(module.id(), module) != null) {
                throw new IllegalArgumentException("Duplicate module ID: " + module.id());
            }
        }
        Properties properties = new Properties();
        properties.load(reader);
        Map<String, Flags> moduleRules = new HashMap<>();
        Map<String, Flags> itemRules = new HashMap<>();
        for (String key : properties.stringPropertyNames()) {
            String[] tokens = key.split("\\.", -1);
            boolean item = tokens.length == 4 && "item".equals(tokens[0]);
            boolean module = tokens.length == 3 && "module".equals(tokens[0]);
            if (!item && !module) {
                throw new IllegalArgumentException("Unsupported policy key: " + key);
            }
            String moduleId = tokens[1];
            if (!catalog.containsKey(moduleId)) {
                throw new IllegalArgumentException("Unknown module in policy: " + moduleId);
            }
            String setting = tokens[tokens.length - 1];
            if (!"guide-visible".equals(setting) && !"player-crafting".equals(setting)) {
                throw new IllegalArgumentException("Unknown policy setting: " + key);
            }
            String raw = properties.getProperty(key);
            if (!"true".equalsIgnoreCase(raw) && !"false".equalsIgnoreCase(raw)) {
                throw new IllegalArgumentException("Expected true or false for " + key);
            }
            boolean value = Boolean.parseBoolean(raw);
            if (module) {
                moduleRules.put(moduleId, moduleRules.getOrDefault(moduleId, Flags.DEFAULT).set(setting, value));
            } else {
                String itemId = normalizedItemId(tokens[2]);
                String itemKey = moduleId + "/" + itemId;
                itemRules.put(itemKey, itemRules.getOrDefault(itemKey, Flags.DEFAULT).set(setting, value));
            }
        }
        return new PolicyRules(catalog, moduleRules, itemRules);
    }

    public Decision guideVisible(String moduleId, String itemId, Actor actor) {
        Objects.requireNonNull(actor, "actor");
        if (actor == Actor.OP) return new Decision(true, "OP guide access");
        if (actor == Actor.AUTOMATION) throw new IllegalArgumentException("Automated machines do not open a Guide");
        Flags parent = getModuleFlags(moduleId);
        if (!parent.guideVisible()) return new Decision(false, "Addon hidden from players");
        if (!getItemFlags(moduleId, itemId).guideVisible()) {
            return new Decision(false, "Item hidden from players");
        }
        return new Decision(true, "Visible to players");
    }

    public Decision manualCraftingAllowed(String moduleId, String itemId, Actor actor) {
        Objects.requireNonNull(actor, "actor");
        if (actor == Actor.OP) return new Decision(true, "OP crafting access");
        if (actor == Actor.AUTOMATION) return new Decision(true, "Automation is not player crafting");
        Flags parent = getModuleFlags(moduleId);
        if (!parent.playerCrafting()) return new Decision(false, "Player crafting disabled for addon");
        if (!getItemFlags(moduleId, itemId).playerCrafting()) {
            return new Decision(false, "Player crafting disabled for item");
        }
        return new Decision(true, "Player crafting permitted");
    }

    private Flags getModuleFlags(String moduleId) {
        requireModule(moduleId);
        return moduleRules.getOrDefault(moduleId, Flags.DEFAULT);
    }

    private Flags getItemFlags(String moduleId, String itemId) {
        requireModule(moduleId);
        return itemRules.getOrDefault(moduleId + "/" + normalizedItemId(itemId), Flags.DEFAULT);
    }

    private void requireModule(String moduleId) {
        if (!catalog.containsKey(moduleId)) {
            throw new IllegalArgumentException("Unknown addon module: " + moduleId);
        }
    }

    private static String normalizedItemId(String itemId) {
        Objects.requireNonNull(itemId, "itemId");
        if (!itemId.matches("[A-Za-z0-9_:-]+")) {
            throw new IllegalArgumentException("Invalid Slimefun item ID: " + itemId);
        }
        return itemId.toUpperCase(Locale.ROOT);
    }
}
