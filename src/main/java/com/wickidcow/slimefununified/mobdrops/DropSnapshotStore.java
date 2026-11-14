package com.wickidcow.slimefununified.mobdrops;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Lifecycle-neutral configuration publication boundary for a future MobDrops adapter.
 * Parsing and validation finish before publish(). Event handlers capture one snapshot,
 * never a mutable collection being repopulated by a concurrent reload.
 *
 * This does not register events, change drop probabilities, or import MobDrops itself.
 */
public final class DropSnapshotStore<T> {
    private final AtomicReference<List<T>> current = new AtomicReference<>(List.of());

    public List<T> snapshot() {
        return current.get();
    }

    /** Rejects null collections/elements without replacing the previous snapshot. */
    public void publish(List<? extends T> validatedRules) {
        Objects.requireNonNull(validatedRules, "validatedRules");
        List<T> copy = new ArrayList<>(validatedRules.size());
        for (T rule : validatedRules) {
            copy.add(Objects.requireNonNull(rule, "drop rule"));
        }
        current.set(List.copyOf(copy));
    }
}
