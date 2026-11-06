package com.wickidcow.slimefununified.runtime;

import io.github.thebusybiscuit.slimefun4.api.events.AncientAltarCraftEvent;
import io.github.thebusybiscuit.slimefun4.api.events.MultiBlockCraftEvent;
import io.github.thebusybiscuit.slimefun4.implementation.Slimefun;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.CraftItemEvent;
import org.bukkit.inventory.ItemStack;

/**
 * Initial player-only crafting interception. Automated crafters are intentionally untouched.
 * Custom addon manufacturing paths are NOT yet comprehensively covered.
 */
public final class UnifiedCraftingListener implements Listener {
    public UnifiedCraftingListener(Slimefun plugin) {
        plugin.getServer().getPluginManager().registerEvents(this, plugin);
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onMultiblock(MultiBlockCraftEvent event) {
        if (UnifiedRuntime.denyPlayerCraft(event.getPlayer(), event.getOutput())) {
            event.setCancelled(true);
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onAltar(AncientAltarCraftEvent event) {
        if (UnifiedRuntime.denyPlayerCraft(event.getPlayer(), event.getItem())) {
            event.setCancelled(true);
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onWorkbench(CraftItemEvent event) {
        if (!(event.getWhoClicked() instanceof Player player)) return;
        ItemStack output = event.getInventory().getResult();
        if (output == null) output = event.getRecipe().getResult();
        if (UnifiedRuntime.denyPlayerCraft(player, output)) {
            event.setCancelled(true);
        }
    }
}
