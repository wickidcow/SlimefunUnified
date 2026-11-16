package com.wickidcow.slimefununified.mobdrops;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;

public final class DropSnapshotStoreSelfTest {
    public static void main(String[] args) throws Exception {
        var store = new DropSnapshotStore<String>();
        assert store.snapshot().isEmpty();
        var source = new ArrayList<>(List.of("first", "second"));
        store.publish(source);
        var old = store.snapshot();
        source.clear();
        assert old.equals(List.of("first", "second"));
        try { old.add("invalid"); throw new AssertionError("mutable snapshot"); }
        catch (UnsupportedOperationException expected) { }
        try { store.publish(Arrays.asList("new", null)); throw new AssertionError("accepted null rule"); }
        catch (NullPointerException expected) { }
        assert store.snapshot() == old;
        var mutable = new StringBuilder("original");
        store.publishMapped(List.of(mutable), value -> value.toString());
        var mapped = store.snapshot();
        mutable.append("-changed");
        assert mapped.equals(List.of("original"));
        try { store.publishMapped(List.of("valid", "bad"), value -> {
            if (value.equals("bad")) throw new IllegalArgumentException("bad rule");
            return value;
        }); throw new AssertionError("accepted failed mapping"); }
        catch (IllegalArgumentException expected) { }
        assert store.snapshot() == mapped;
        try { store.publishMapped(List.of("bad"), value -> null); throw new AssertionError("accepted null mapping"); }
        catch (NullPointerException expected) { }
        assert store.snapshot() == mapped;
        // A failed reload must never publish even its successfully mapped prefix.
        var beforeFailure = store.snapshot();
        try {
            store.publishMapped(List.of("good", "reject", "later"), value -> {
                if (value.equals("reject")) throw new IllegalStateException("invalid config");
                return value.toUpperCase(java.util.Locale.ROOT);
            });
            throw new AssertionError("accepted partially mapped reload");
        } catch (IllegalStateException expected) { }
        assert store.snapshot() == beforeFailure;
        try {
            store.<String>publishMapped(null, value -> value);
            throw new AssertionError("accepted null input");
        } catch (NullPointerException expected) { }
        assert store.snapshot() == beforeFailure;
        try {
            store.publishMapped(List.of("valid"), null);
            throw new AssertionError("accepted null mapper");
        } catch (NullPointerException expected) { }
        assert store.snapshot() == beforeFailure;
        store.publishMapped(List.<String>of(), value -> value);
        assert store.snapshot().isEmpty();
        assert beforeFailure.equals(List.of("original"));
        store.publish(List.of("first", "second"));
        var start = new CountDownLatch(1);
        var failure = new AtomicReference<Throwable>();
        Thread reader = new Thread(() -> {
            try {
                start.await();
                for (int i = 0; i < 100_000; i++) {
                    List<String> observed = store.snapshot();
                    if (!(observed.equals(List.of("first", "second"))
                            || observed.equals(List.of("replacement")))) {
                        throw new AssertionError("partial snapshot: " + observed);
                    }
                }
            } catch (Throwable error) { failure.set(error); }
        });
        reader.start();
        start.countDown();
        for (int i = 0; i < 1000; i++) store.publish(List.of("replacement"));
        reader.join();
        if (failure.get() != null) throw new AssertionError(failure.get());
        // Readers must see one complete generation even while a mapped reload is converting.
        var mappedStore = new DropSnapshotStore<String>();
        mappedStore.publish(List.of("old-A", "old-B"));
        var mappingStarted = new CountDownLatch(1);
        var finishMapping = new CountDownLatch(1);
        var mappedFailure = new AtomicReference<Throwable>();
        Thread writer = new Thread(() -> {
            try {
                mappedStore.publishMapped(List.of("new-A", "new-B"), value -> {
                    if (value.equals("new-B")) {
                        mappingStarted.countDown();
                        try { finishMapping.await(); }
                        catch (InterruptedException interrupted) {
                            Thread.currentThread().interrupt();
                            throw new IllegalStateException(interrupted);
                        }
                    }
                    return value;
                });
            } catch (Throwable error) { mappedFailure.set(error); }
        });
        writer.start();
        mappingStarted.await();
        for (int i = 0; i < 1000; i++) {
            assert mappedStore.snapshot().equals(List.of("old-A", "old-B"));
        }
        finishMapping.countDown();
        writer.join();
        if (mappedFailure.get() != null) throw new AssertionError(mappedFailure.get());
        assert mappedStore.snapshot().equals(List.of("new-A", "new-B"));
        assert old.equals(List.of("first", "second"));
        // Shutdown drops future rules but does not mutate an event's captured generation.
        var inFlight = mappedStore.snapshot();
        mappedStore.clear();
        assert mappedStore.snapshot().isEmpty();
        assert inFlight.equals(List.of("new-A", "new-B"));
        mappedStore.clear(); // Idempotent on repeated disable.
        assert mappedStore.snapshot().isEmpty();
        mappedStore.publish(List.of("re-enabled"));
        assert mappedStore.snapshot().equals(List.of("re-enabled"));
        System.out.println("MobDrops immutable snapshot publication self-test passed");
    }
}
