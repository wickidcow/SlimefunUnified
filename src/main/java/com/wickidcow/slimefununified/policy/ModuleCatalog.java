package com.wickidcow.slimefununified.policy;

import java.util.List;

/** Candidates only: this catalog does not register or import any addon. */
public final class ModuleCatalog {
    private ModuleCatalog() {}

    public static List<AddonModule> candidates() {
        return List.of(
                new AddonModule("slimefun", "Slimefun Core", "TheBusyBiscuit and Slimefun contributors",
                        "https://github.com/wickidcow/Slimefun-Legacy"),
                new AddonModule("extraheads", "ExtraHeads",
                        "TheBusyBiscuit; ybw0014 / Slimefun Addon Community",
                        "https://github.com/wickidcow/SF_ExtraHeads"),
                new AddonModule("souljars", "SoulJars", "TheBusyBiscuit and SoulJars community contributors",
                        "https://github.com/wickidcow/SF_SoulJars"),
                new AddonModule("fluffymachines", "FluffyMachines", "NCBPFluffyBear and FluffyMachines contributors",
                        "https://github.com/wickidcow/SF_FluffyMachines"),
                new AddonModule("infinityexpansion2", "InfinityExpansion2",
                        "Mooy1; GuizhanCraft and InfinityExpansion2 contributors",
                        "https://github.com/wickidcow/SF_InfinityExpansion2"),
                new AddonModule("networks", "Networks", "Sefiraat and NetworksExpansion contributors",
                        "https://github.com/wickidcow/SF_NetworksExp"),
                new AddonModule("supreme", "Supreme", "RelativoBR, Especttra, WilianSantosBR, Mynothauro and contributors",
                        "https://github.com/wickidcow/SF_Supreme"),
                new AddonModule("justenoughguide", "JustEnoughGuide", "balugaq and JEG contributors",
                        "https://github.com/wickidcow/SF_JustEnoughGuide")
        );
    }
}
