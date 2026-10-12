# Contributing to the Believer Project

Thanks for your interest in contributing to the Believer project! Contributions such as bug fixes, documentation improvements, configuration changes, and new features are welcome.

**Original repository:** `https://github.com/SpicyTenderloin/believer`

You will need a GitHub account and Git installed on your computer. Contributions are made using **forks and pull requests**. You do **not** need write access to the original repository. Changes to the original project are reviewed before they are merged.

## Before you start

This repo contains systems engineering documentation, configuration files, user manuals, and governance documentation for developing and maintaining a fixed-wing UAV system. To contribute effectively, there are a few things worth knowing before you dive in.

This repo is also explicitly designed around an AI-in-the-loop workflow, which shapes how it's organised. **`context/` is built primarily for AI agents, not people.** It holds the project's working memory - conventions, decision history, open items, a running changelog - so an AI coding agent (Claude Code, Codex, or similar) can pick up full context at the start of a session instead of re-deriving it. You can read and edit these files directly, but the repo's workflow is designed around having an agent in the loop: when something changes, the agent updates `docs/`, logs the change in `context/CHANGELOG.md`, and records any decision history or new open items in the right `context/` file, all in the same pass. Doing this entirely by hand means remembering to make all of those updates yourself - **the easiest way to contribute correctly is to point an AI agent at [`context/startup-prompt.md`](context/startup-prompt.md) and work through it**, even if you're the one deciding what should change.

- **Read [`context/startup-prompt.md`](context/startup-prompt.md) first**, whether you're working directly or through an agent. It is the single entry point for understanding the project: a summary, the read-order for the rest of `context/`, and a map of the key documents under `docs/`.
- **Follow [`context/style-guide.md`](context/style-guide.md) for any change under `docs/`.** The short version: `docs/` states current, as-built facts cleanly, with no inline decision history or provenance narration - that content belongs in `context/project-notes.md` instead. See the style guide for the full formatting rules.
- **Log every change to a repo document in [`context/CHANGELOG.md`](context/CHANGELOG.md), in the same commit as the change itself.** See [`context/directives.md`](context/directives.md) for this and the other working conventions (file organisation, source-material handling).
- **Changes affecting PX4 configuration, parameters, or flight controls are safety-critical.** Explain the safety implications and what testing was performed in your pull request, and clearly identify anything not tested - see `docs/project/build-checklist.md` for how this project tracks flight-readiness priority (Critical / Urgent / Non-critical).
- **AI use on this project is open and acknowledged** - see [`context/academic-integrity.md`](context/academic-integrity.md) for the QUT policy context if you're a QUT student contributing as part of coursework.

## How to contribute

### 1. Fork the repository on GitHub

1. Sign in to your GitHub account.
2. Open the original Believer repository using the URL above.
3. Click **Fork** (near the top-right of the page), then **Create fork**.

You now have your own copy of the repository under your GitHub account.

### 2. Clone your fork to your computer

1. Open **your fork** on GitHub (not the original repository).
2. Click **Code** and copy its **HTTPS** URL.
3. In a terminal, run:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_FORK_NAME.git
cd YOUR_FORK_NAME
```

Replace `YOUR_USERNAME` and `YOUR_FORK_NAME` with the values shown in **your fork's** URL. You can also paste the HTTPS URL directly into the `git clone` command.

### 3. Create a branch for your changes

Create a separate branch so your work stays independent of the fork's default branch:

```bash
git switch -c describe-your-change
```

For example, use `fix-airspeed-config` or `improve-documentation`. Use a new branch for each separate contribution.

### 4. Make and test your changes

Edit the files on your computer, using your preferred editor or IDE.

- Keep changes focused on one fix or feature per pull request.
- Check your changes for errors and test them where practical.
- For changes affecting PX4, flight controls, or aircraft configuration, explain any safety implications and what testing was performed. Clearly identify anything **not** tested.
- For changes to any file under `docs/` or `context/`, follow [`context/style-guide.md`](context/style-guide.md) and add an entry to [`context/CHANGELOG.md`](context/CHANGELOG.md).
- Do not commit passwords, API keys, private information, or unnecessary large files.

### 5. Commit your changes

In your terminal, review what you changed:

```bash
git status
git diff
```

Then stage and commit your changes:

```bash
git add -A
git commit -m "Describe the change briefly"
```

Before committing, use `git status` to make sure you are not including unrelated or sensitive files.

### 6. Push your branch to your fork

```bash
git push -u origin describe-your-change
```

Use the same branch name you created in Step 3. This uploads your changes to **your fork** on GitHub, not the original Believer repository.

### 7. Open a pull request

1. Open **your fork** on GitHub.
2. Click **Compare & pull request** if GitHub displays that option. Otherwise, visit the original repository's **Pull requests** tab and click **New pull request**, then **compare across forks** if needed.
3. Check that the **base repository** is the **original Believer repository**, and the **base branch** is its default branch (usually `main`).
4. Check that the **head fork** is **your fork**, and the **compare branch** is the branch containing your changes.
5. Write a clear title and description covering:
   - What you changed and why.
   - How you tested it (or why you could not test it).
   - Any relevant PX4, hardware, or configuration details, particularly for safety-critical changes.
6. Click **Create pull request**.

The project maintainer will review your changes and may ask questions or request adjustments. **Creating a pull request does not change the original repository.** Your changes are only incorporated if the pull request is merged.

### 8. Respond to review feedback (if needed)

If changes are requested, make them on the **same local branch**, then commit and push again:

```bash
git add -A
git commit -m "Address review feedback"
git push
```

Your existing pull request will update automatically. There is no need to open a second one.

## Contributing again later

You can keep your fork and reuse it for future contributions. Before starting a new contribution, go to your fork on GitHub, select its default branch, and use **Sync fork → Update branch** to bring in updates from the original repository. On your computer, switch to your local default branch, run `git pull` to update it, and create a **new feature branch** for the next change.

## Questions or larger proposals

For substantial changes, especially those affecting flight behaviour or safety, consider opening a GitHub **Issue** in the original repository first to discuss the approach before implementing it.

---

**Summary:** Fork → Clone → Branch → Edit → Commit → Push to your fork → Pull request → Review → Merge (if approved).

**GitHub references:** [Contributing to open source](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-open-source) · [Creating a pull request from a fork](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request-from-a-fork)
