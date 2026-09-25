# Contributing to Awesome Quantum Machine Learning

Thank you for taking the time to contribute to **Awesome Quantum Machine Learning**! We welcome contributions from quantum researchers, software engineers, students, and enthusiasts worldwide.

Please take a moment to review these guidelines before submitting a pull request or creating an issue.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainer (`qml-maintainer`) at `qml-maintainer@users.noreply.github.com`.

## Guidelines for Contributing

To maintain high quality and consistency across the repository, please adhere to the following strict guidelines when proposing a new resource:

### Formatting Rules

1. **Item Format**: Every added resource must strictly follow this format:
   ```markdown
   - [Resource Name](URL) - One clear, concise sentence description ending with a period.
   ```
2. **Alphabetical Ordering**: Items in every section must be listed in **strict alphabetical order** by resource title.
3. **Single Sentence Description**: The description must be exactly one informative sentence that clearly explains what the resource provides, ending with a period `.`.
4. **Valid & Active Links**: Ensure that all URLs use `https://` where available and point directly to active, official, or high-relevance pages. Broken or dead links will cause CI build checks to fail.
5. **No Redundant Words**: Avoid starting descriptions with phrases like "A framework that..." or "This paper is about...". Keep descriptions direct and objective.
6. **Awesome Quality Standards**: Resources must be high-quality, reputable, and directly relevant to Quantum Machine Learning (QML). Self-promotional or low-effort content will be rejected.

---

## How to Propose a Contribution

### Adding a Resource via Pull Request

1. **Fork the Repository**: Create your own fork of this repository on GitHub.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b add/my-new-resource
   ```
3. **Modify `README.md`**:
   - Locate the most appropriate section/category for your entry.
   - Insert the item maintaining **alphabetical order**.
   - Ensure trailing periods and proper formatting.
4. **Test Your Changes**: Verify links and check for syntax errors locally.
5. **Commit Your Changes**:
   ```bash
   git commit -m "Add [Resource Name] to [Category Name]"
   ```
6. **Push and Open a Pull Request**: Push your branch to GitHub and open a Pull Request against the `main` branch.
7. **Fill out the Pull Request Template**: Complete all items in the checklist provided in the PR template.

### Suggesting Resources via Issue

If you cannot submit a PR, feel free to open an issue using the [Add Resource Issue Template](.github/ISSUE_TEMPLATE/add-resource.md).

---

## Automated Checks & Local Validation

To keep the repository clean and standardized, we use automated checks in CI/CD and provide a local validation script.

### Running the Linter Locally

Before submitting your Pull Request, you can validate your changes locally by running our Python linter script:

```bash
python scripts/validate_readme.py
```

This script verifies that:
- Every entry strictly follows the `- [Name](URL) - Description.` format.
- Every description ends with a period (`.`).
- Entries within each category are sorted in **strict alphabetical order**.

### CI/CD Workflows

Every Pull Request automatically triggers two GitHub Actions workflows:
1. **README Linter (`lint.yml`)**: Executes `scripts/validate_readme.py` to ensure proper formatting and alphabetical ordering.
2. **Link Checker (`check-links.yml`)**: Executes `lychee-action` to ensure all URLs are active and accessible.

Thank you for helping us curate the best Quantum Machine Learning resources!
