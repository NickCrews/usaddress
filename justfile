# List justfile recipes
default:
    just --list

# Update dependencies
update:
    pdm update --update-all --dev

# Lint
lint:
    pdm run ruff

# Format
fmt:
    pdm run ruff format
    pdm run ruff --fix .


# Train the CRF model
train:
    parserator train training/labeled.xml usaddress

# Build wheels and sdists to dist/
build *ARGS:
    rm usaddress/usaddr.crfsuite
    just train
    pdm build {{ARGS}}

# Publish to GitHub Releases
release-gh TAG:
    git tag -a {{TAG}} -m "{{TAG}}" || true
    git push origin {{TAG}} || true
    gh release create {{TAG}} --title "{{TAG}}" --notes "Release {{TAG}}" --latest dist/*