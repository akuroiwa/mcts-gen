# Tasks for UV and FastMCP Documentation Update (with Translation)

## Task List

1.  **Update `README.md` (English)**
    -   **Description**: Add a new section to the main `README.md` file detailing the environment setup using `uv` and the `fastmcp install gemini-cli` command.
    -   **File**: `/home/akihiro/文書/develop/git/akuroiwa/mcts-gen/README.md`

2.  **Update `docs/quickstart.rst` (English)**
    -   **Description**: Add the same setup instructions to the `docs/quickstart.rst` file.
    -   **File**: `/home/akihiro/文書/develop/git/akuroiwa/mcts-gen/docs/quickstart.rst`

3.  **Update Translation Source & PO Files**
    -   **Description**: Run commands to extract new strings from the English `.rst` file and update the Japanese `.po` file.
    -   **Command**: `cd /home/akihiro/文書/develop/git/akuroiwa/mcts-gen/docs && make gettext && sphinx-intl update --language=ja`
    -   **Verification**: Check that `docs/locales/ja/LC_MESSAGES/quickstart.po` is updated with new `msgid` entries.

4.  **Add Japanese Translation to `quickstart.po`**
    -   **Description**: Edit `docs/locales/ja/LC_MESSAGES/quickstart.po` to add the Japanese translation for the new sections, using the content from the WordPress article.
    -   **File**: `/home/akihiro/文書/develop/git/akuroiwa/mcts-gen/docs/locales/ja/LC_MESSAGES/quickstart.po`

5.  **Build and Verify HTML Documentation**
    -   **Description**: Compile the translations and rebuild the entire HTML documentation to ensure all changes are correctly applied without errors.
    -   **Command**: `cd /home/akihiro/文書/develop/git/akuroiwa/mcts-gen/docs && sphinx-intl build && make clean && make html`
    -   **Verification**: Check the generated HTML files in `docs/_build/html/ja/`.