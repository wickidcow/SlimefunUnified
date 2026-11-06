package io.github.thebusybiscuit.extraheads;

import com.wickidcow.slimefununified.runtime.UnifiedRuntime;
import io.github.thebusybiscuit.extraheads.listeners.HeadListener;
import io.github.thebusybiscuit.extraheads.setup.ItemSetup;
import io.github.thebusybiscuit.extraheads.setup.Registry;
import io.github.thebusybiscuit.slimefun4.api.SlimefunAddon;
import io.github.thebusybiscuit.slimefun4.implementation.Slimefun;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.annotation.Nonnull;
import org.bukkit.Server;
import org.bukkit.configuration.InvalidConfigurationException;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

/**
 * SlimefunUnified adapter for TheBusyBiscuit's MIT-licensed ExtraHeads addon.
 * The original addon and its IDs are preserved; its separate JavaPlugin bootstrap
 * is replaced by this facade so the Unified distribution only has one plugin.yml.
 */
public final class ExtraHeads implements SlimefunAddon {
    private static ExtraHeads instance;
    private final Slimefun core;
    private final Path configPath;
    private final YamlConfiguration config;
    private final Registry registry;

    private ExtraHeads(Slimefun core, Path configPath, YamlConfiguration config) {
        this.core = core;
        this.configPath = configPath;
        this.config = config;
        this.registry = new Registry(config);
    }

    public static void start(Slimefun core) {
        // Do not double-register old persisted item IDs if a standalone ExtraHeads is installed.
        if (core.getServer().getPluginManager().getPlugin("ExtraHeads") != null) {
            core.getLogger().warning("Standalone ExtraHeads plugin detected. Unified ExtraHeads module is skipped; "
                    + "remove the duplicate only after backing up and testing your server.");
            return;
        }

        try {
            Path configPath = new File(core.getDataFolder().getParentFile(), "ExtraHeads/config.yml").toPath();
            if (!Files.isRegularFile(configPath)) {
                Files.createDirectories(configPath.getParent());
                try (InputStream source = core.getResource("unified/addons/extraheads/config.yml")) {
                    if (source == null) throw new IOException("Missing original ExtraHeads default configuration");
                    Files.copy(source, configPath);
                }
            }
            YamlConfiguration config = new YamlConfiguration();
            config.load(configPath.toFile());
            ExtraHeads addon = new ExtraHeads(core, configPath, config);
            instance = addon;
            ItemSetup.setup();
            // Register addon identity, not a JavaPlugin name (all modules share one JavaPlugin).
            UnifiedRuntime.registerBundledAddon("extraheads", addon);
            new HeadListener(addon);
            core.getLogger().info("SlimefunUnified: ExtraHeads module registered "
                    + addon.registry.getHeads().size() + " mob heads with historical item IDs.");
        } catch (IOException | InvalidConfigurationException | IllegalArgumentException exception) {
            instance = null;
            core.getLogger().log(Level.SEVERE,
                    "SlimefunUnified ExtraHeads module could not initialize; existing data was not deleted", exception);
        }
    }

    public static ExtraHeads getInstance() {
        if (instance == null) throw new IllegalStateException("Unified ExtraHeads module not initialized");
        return instance;
    }

    public static Registry getRegistry() {
        return getInstance().registry;
    }

    public Server getServer() {
        return core.getServer();
    }

    public Logger getLogger() {
        return core.getLogger();
    }

    public YamlConfiguration getConfig() {
        return config;
    }

    /** Persist original plugin config path without altering its settings or contents. */
    public void saveConfig() {
        try {
            Path temp = Files.createTempFile(configPath.getParent(), "extraheads-", ".tmp");
            try {
                Files.writeString(temp, config.saveToString(), StandardCharsets.UTF_8);
                try {
                    Files.move(temp, configPath, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);
                } catch (AtomicMoveNotSupportedException ignored) {
                    Files.move(temp, configPath, StandardCopyOption.REPLACE_EXISTING);
                }
            } finally {
                Files.deleteIfExists(temp);
            }
        } catch (IOException exception) {
            core.getLogger().log(Level.SEVERE, "Could not save historical ExtraHeads config", exception);
        }
    }

    @Override
    @Nonnull
    public JavaPlugin getJavaPlugin() {
        return core;
    }

    @Override
    @Nonnull
    public String getName() {
        return "ExtraHeads";
    }

    @Override
    @Nonnull
    public String getBugTrackerURL() {
        return "https://github.com/wickidcow/SF_ExtraHeads/issues";
    }
}
