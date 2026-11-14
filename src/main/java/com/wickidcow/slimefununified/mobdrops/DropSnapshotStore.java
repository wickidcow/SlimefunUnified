package com.wickidcow.slimefununified.mobdrops;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Function;

/**
 * Lifecycle-neutral configuration publication boundary for a future MobDrops adapter.
 * Parsing and validation finish before publication. Event handlers capture one snapshot.
 * Rule objects must be immutable, or copied into immutable representations by the mapper.
 * This does not register events, change drop probabilities, or import MobDrops itself.
 */
public final class DropSnapshotStore<T> {
    private final AtomicReference<List<T>> current = new AtomicReference<>(List.of());

    public List<T> snapshot() {
        return current.get();
    }

    /** Publishes an immutable list. Elements must themselves be immutable. */
    public void publish(List<? extends T> validatedRules) {
        publishMapped(validatedRules, Function.identity());
    }

    /**
     * Converts mutable parsed rules to immutable event-safe rules before publishing.
     * If conversion throws or returns null, the previous snapshot is retained.
     * Mapper output must be deeply immutable; copying the list alone is insufficient.
     */
    public <S> void publishMapped(List<? extends S> parsedRules, Function<? super S, ? extends T> immutableMapper) {
        Objects.requireNonNull(parsedRules, "parsedRules");
        Objects.requireNonNull(immutableMapper, "immutableMapper");
        List<T> copy = new ArrayList<>(parsedRules.size());
        for (S rule : parsedRules) {
            copy.add(Objects.requireNonNull(immutableMapper.apply(Objects.requireNonNull(rule, "drop rule")), "mapped drop rule"));
        }
        current.set(List.copyOf(copy));
    }
}
