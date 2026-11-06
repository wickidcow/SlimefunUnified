package com.wickidcow.slimefununified.policy;

import java.util.Objects;

public record AddonModule(String id, String displayName, String originalCreators, String maintainedSource) {
    public AddonModule {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(displayName, "displayName");
        Objects.requireNonNull(originalCreators, "originalCreators");
        Objects.requireNonNull(maintainedSource, "maintainedSource");
        if (!id.matches("[a-z][a-z0-9_]*")) {
            throw new IllegalArgumentException("Invalid stable module ID: " + id);
        }
        if (displayName.isBlank() || originalCreators.isBlank() || maintainedSource.isBlank()) {
            throw new IllegalArgumentException("Display name, credits and source are required for " + id);
        }
    }
}
