package com.wickidcow.slimefununified.policy;

import java.io.StringReader;
import java.util.List;

public final class PolicyRulesSelfTest {
    private PolicyRulesSelfTest() {}

    private static void check(boolean condition, String failure) {
        if (!condition) throw new AssertionError(failure);
    }

    private static void expectIllegal(String name, Runnable action) {
        try {
            action.run();
        } catch (IllegalArgumentException expected) {
            return;
        }
        throw new AssertionError("Should reject: " + name);
    }

    public static void main(String[] args) throws Exception {
        var modules = ModuleCatalog.candidates();
        PolicyRules open = PolicyRules.fromProperties(new StringReader(""), modules);
        check(open.guideVisible("fluffymachines", "FLUFFY_BARREL", PolicyRules.Actor.PLAYER).allowed(),
                "Default module guide access");
        check(open.manualCraftingAllowed("fluffymachines", "FLUFFY_BARREL",
                PolicyRules.Actor.PLAYER).allowed(), "Default player crafting");

        PolicyRules hidden = PolicyRules.fromProperties(new StringReader("""
                module.fluffymachines.guide-visible=false
                module.fluffymachines.player-crafting=false
                item.infinityexpansion2.COW_HEARDER.guide-visible=false
                item.infinityexpansion2.COW_HEARDER.player-crafting=false
                item.fluffymachines.FLUFFY_BARREL.guide-visible=true
                item.fluffymachines.FLUFFY_BARREL.player-crafting=true
                """), modules);

        check(!hidden.guideVisible("fluffymachines", "FLUFFY_BARREL", PolicyRules.Actor.PLAYER).allowed(),
                "Parent hidden wins over item allow");
        check(!hidden.manualCraftingAllowed("fluffymachines", "FLUFFY_BARREL",
                PolicyRules.Actor.PLAYER).allowed(), "Parent craft deny wins over item allow");
        check(hidden.guideVisible("fluffymachines", "FLUFFY_BARREL", PolicyRules.Actor.OP).allowed(),
                "OP still sees addon");
        check(hidden.manualCraftingAllowed("fluffymachines", "FLUFFY_BARREL",
                PolicyRules.Actor.OP).allowed(), "OP still crafts addon");
        check(hidden.manualCraftingAllowed("fluffymachines", "FLUFFY_BARREL",
                PolicyRules.Actor.AUTOMATION).allowed(), "Machine automation unaffected");
        check(!hidden.guideVisible("infinityexpansion2", "cow_hearder",
                PolicyRules.Actor.PLAYER).allowed(), "Case normalization and individual hiding");
        check(!hidden.manualCraftingAllowed("infinityexpansion2", "COW_HEARDER",
                PolicyRules.Actor.PLAYER).allowed(), "Individual player crafting deny");
        check(hidden.manualCraftingAllowed("infinityexpansion2", "OTHER_ITEM",
                PolicyRules.Actor.PLAYER).allowed(), "Unrestricted items keep working");
        check(hidden.guideVisible("slimefun", "BATTERY", PolicyRules.Actor.PLAYER).allowed(),
                "No core breakage");

        expectIllegal("unknown module", () -> hidden.guideVisible("missing", "ITEM", PolicyRules.Actor.PLAYER));
        expectIllegal("bad item ID", () -> hidden.guideVisible("slimefun", "?", PolicyRules.Actor.PLAYER));
        expectIllegal("machine Guide", () -> hidden.guideVisible("slimefun", "BATTERY",
                PolicyRules.Actor.AUTOMATION));
        expectIllegal("module descriptor without credits", () ->
                new AddonModule("bad", "Bad", "", "https://example.com"));
        expectIllegal("duplicate catalog ID", () -> {
            try {
                PolicyRules.fromProperties(new StringReader(""), List.of(modules.get(0), modules.get(0)));
            } catch (java.io.IOException impossible) {
                throw new IllegalStateException(impossible);
            }
        });
        for (String bad : List.of("module.missing.guide-visible=true",
                "module.fluffymachines.player-crafting=whatever",
                "module.fluffymachines.unknown=true",
                "item.fluffymachines.BAD!.guide-visible=false",
                "module.fluffymachines.guide-visible=true\nunsupported.value=true")) {
            expectIllegal("invalid config: " + bad, () -> {
                try {
                    PolicyRules.fromProperties(new StringReader(bad), modules);
                } catch (java.io.IOException impossible) {
                    throw new IllegalStateException(impossible);
                }
            });
        }
        System.out.println("SlimefunUnified policy: all 18 scenarios passed.");
    }
}
