# NPM Maintainer Email Harvest (Educational Tool)

## Overview

This project demonstrates how attackers historically harvested maintainer email addresses from the public npm registry API. Due to recent security improvements, the npm registry no longer exposes maintainer emails via its API. This repository is for educational and research purposes only, to raise awareness about past vulnerabilities and the importance of securing developer information.

## ⚠️ Disclaimer

- **This code is provided strictly for educational and research purposes.**
- **Do not use this tool for malicious purposes or to violate the privacy of others.**
- The maintainer email harvesting method shown here is no longer effective due to npm's security updates.
- The authors and contributors are not responsible for any misuse of this code.

## How It Worked (Historically)

Attackers could query the npm registry API for any package and receive a list of maintainers, including their email addresses, in the `maintainers` field. This allowed for mass-harvesting of emails for phishing and spam campaigns. As of 2021, npm removed public access to maintainer emails via the API.

## How to Use

1. **Install dependencies:**
   ```bash
   pip install requests
   ```
2. **Run the script:**
   ```bash
   python main.py <package-name>
   ```
   - If no package name is provided, the script defaults to `chalk` as an example.

3. **Expected Output:**
   - If the `maintainers` field is present (rare today), it will display maintainer names and emails.
   - Otherwise, it will show author and version info, demonstrating the API call works but emails are not exposed.

## Example

```bash
python main.py express
```

## Why This Matters

- **Security Awareness:** Shows how easily sensitive information was once accessible.
- **Research:** Useful for understanding the evolution of open source ecosystem security.
- **Education:** Demonstrates the importance of responsible data handling and privacy.


## License

This project is licensed for educational and research use only. See the repository license for details.
