# Contributing

## Working with the function

Specific instructions for building / testing the function can be found in [function/README.md](./function/README.md).

## Testing the package build

The lambda package build can be tested locally by following the steps in the `package-build` job of the `.github/workflows/pull-request.yml` workflow. The job uses [moto](https://docs.getmoto.org/en/latest/index.html) to remove the need to authenticate to AWS.

## Updating documentation

The README can be automatically updated using [terraform-docs](https://github.com/terraform-docs/terraform-docs).

```shell
docker run --rm --volume "$(pwd):/terraform-docs" -u $(id -u) quay.io/terraform-docs/terraform-docs:0.18.0 markdown table --indent 2 --output-mode inject --output-file README.md --output-template '<!-- BEGIN_TF_DOCS -->\n{{ .Content }}\n<!-- END_TF_DOCS -->' /terraform-docs
```

> N.B. Make sure the following files have been removed before using terraform-docs `.terraform.lock.hcl`.
