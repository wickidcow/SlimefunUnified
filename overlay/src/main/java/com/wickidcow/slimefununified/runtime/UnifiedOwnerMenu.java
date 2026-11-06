package com.wickidcow.slimefununified.runtime;

import com.wickidcow.slimefununified.policy.AddonModule;
import com.wickidcow.slimefununified.policy.ModuleCatalog;
import io.github.bakedlibs.dough.items.CustomItemStack;
import io.github.thebusybiscuit.slimefun4.core.guide.SlimefunGuide;
import io.github.thebusybiscuit.slimefun4.core.guide.SlimefunGuideMode;
import io.github.thebusybiscuit.slimefun4.core.guide.options.SlimefunGuideSettings;
import io.github.thebusybiscuit.slimefun4.utils.ChatUtils;
import io.github.thebusybiscuit.slimefun4.utils.ChestMenuUtils;
import java.util.List;
import me.mrCookieSlime.CSCoreLibPlugin.general.Inventory.ChestMenu;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

/**
 * Slimefun Unified OP area. Every clickable mutation re-checks permission.
 * Candidate addons are shown for credit, but cannot be toggled until truly bundled.
 */
public final class UnifiedOwnerMenu {
    private static final int PAGE_SIZE = 4;

    private UnifiedOwnerMenu() {}

    public static void open(Player player, ItemStack guide) {
        openPage(player, guide, 0);
    }

    private static void openPage(Player player, ItemStack guide, int page) {
        if (!UnifiedRuntime.isOwner(player)) {
            player.sendMessage("§cSlimefun Unified server management requires OP/admin permission.");
            return;
        }
        List<AddonModule> modules = ModuleCatalog.candidates();
        int pageCount = Math.max(1, (modules.size() + PAGE_SIZE - 1) / PAGE_SIZE);
        int currentPage = Math.min(Math.max(0, page), pageCount - 1);
        ItemStack returnGuide = guide == null
                ? SlimefunGuide.getItem(SlimefunGuideMode.SURVIVAL_MODE)
                : guide.clone();

        ChestMenu menu = new ChestMenu("§6§lSlimefun Unified Server Management");
        menu.setSize(54);
        menu.setEmptySlotsClickable(false);
        for (int slot = 0; slot < 54; slot++) {
            menu.addItem(slot, ChestMenuUtils.getBackground(), ChestMenuUtils.getEmptyClickHandler());
        }

        menu.addItem(0, new CustomItemStack(Material.ARROW, "&eBack to Guide Settings"),
                (pl, slot, stack, action) -> {
                    if (UnifiedRuntime.isOwner(pl)) SlimefunGuideSettings.openSettings(pl, returnGuide);
                    return false;
                });
        menu.addItem(4, new CustomItemStack(Material.COMMAND_BLOCK, "&6&lSlimefun Unified",
                "&7Addon code stays loaded; items and machines are retained.",
                "&7Guide visibility and player crafting are independent.",
                "&aOPs retain access to all registered items.",
                UnifiedRuntime.writable() ? "&aSettings storage available" : "&cConfig invalid: see server log"),
                ChestMenuUtils.getEmptyClickHandler());

        for (int index = 0; index < PAGE_SIZE; index++) {
            int itemIndex = currentPage * PAGE_SIZE + index;
            if (itemIndex >= modules.size()) break;
            AddonModule module = modules.get(itemIndex);
            boolean bundled = UnifiedRuntime.isBundled(module.id());
            int start = 9 + index * 9;

            menu.addItem(start, new CustomItemStack(bundled ? Material.BOOKSHELF : Material.BARRIER,
                    "&e" + module.displayName(),
                    "&7Original creators: " + module.originalCreators(),
                    bundled ? "&aBuilt into this development JAR" : "&8Not yet integrated into this JAR"),
                    ChestMenuUtils.getEmptyClickHandler());

            if (bundled) {
                boolean visible = UnifiedRuntime.guideVisibleFlag(module.id());
                menu.addItem(start + 2, new CustomItemStack(visible ? Material.LIME_DYE : Material.GRAY_DYE,
                        "&bPlayer Guide: " + (visible ? "&aVISIBLE" : "&cHIDDEN"),
                        "&7Only affects non-admin Guide discovery.",
                        "&eClick to toggle"),
                        (pl, slot, stack, action) -> {
                            if (!UnifiedRuntime.toggle(pl, module.id(), "guide-visible")) {
                                pl.sendMessage("§cUnified policy was not saved. Check permissions and the console.");
                            }
                            openPage(pl, returnGuide, currentPage);
                            return false;
                        });

                boolean crafting = UnifiedRuntime.craftingFlag(module.id());
                menu.addItem(start + 4, new CustomItemStack(crafting ? Material.CRAFTING_TABLE : Material.BARRIER,
                        "&6Player Crafting: " + (crafting ? "&aALLOWED" : "&cBLOCKED"),
                        "&7OPs and automation remain unaffected.",
                        "&eClick to toggle"),
                        (pl, slot, stack, action) -> {
                            if (!UnifiedRuntime.toggle(pl, module.id(), "player-crafting")) {
                                pl.sendMessage("§cUnified policy was not saved. Check permissions and the console.");
                            }
                            openPage(pl, returnGuide, currentPage);
                            return false;
                        });
            } else {
                menu.addItem(start + 2, new CustomItemStack(Material.GRAY_DYE,
                        "&8Player Guide: unavailable until bundled"),
                        ChestMenuUtils.getEmptyClickHandler());
                menu.addItem(start + 4, new CustomItemStack(Material.GRAY_DYE,
                        "&8Player Crafting: unavailable until bundled"),
                        ChestMenuUtils.getEmptyClickHandler());
            }

            menu.addItem(start + 6, new CustomItemStack(Material.WRITTEN_BOOK,
                    "&eCreator Credits & Project Source",
                    "&7" + module.originalCreators(),
                    "&7" + module.maintainedSource(),
                    "&eClick to open maintained project"),
                    (pl, slot, stack, action) -> {
                        if (UnifiedRuntime.isOwner(pl)) {
                            pl.closeInventory();
                            ChatUtils.sendURL(pl, module.maintainedSource());
                        }
                        return false;
                    });
        }

        menu.addItem(45, new CustomItemStack(Material.ARROW, "&ePrevious Page"),
                (pl, slot, stack, action) -> {
                    if (UnifiedRuntime.isOwner(pl)) openPage(pl, returnGuide, currentPage - 1);
                    return false;
                });
        menu.addItem(53, new CustomItemStack(Material.ARROW, "&eNext Page"),
                (pl, slot, stack, action) -> {
                    if (UnifiedRuntime.isOwner(pl)) openPage(pl, returnGuide, currentPage + 1);
                    return false;
                });
        menu.open(player);
    }
}
