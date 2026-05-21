# Examples

Decks de démonstration pour vérifier rapidement que le skill fonctionne.

| Fichier | Slides | Layouts | Usage |
|---|---|---|---|
| [example_minimal.json](example_minimal.json) | cover + 3 + closing | `hero_stat`, `roadmap`, `text` | Smoke test rapide |
| [example_full.json](example_full.json) | cover + 12 + closing | 11 layouts variés (code-based + template-based) | Couverture étendue, mix mécanismes |

## Lancer la génération

Depuis la racine du projet :

```bash
python aosis-deck-builder/scripts/build_deck.py \
    examples/example_full.json \
    /tmp/example_full.pptx
```

Ou via le script de test global :

```bash
./test_skill.sh
```

Le script lance pytest, génère les deux exemples, et affiche les chemins.

## Ajouter un exemple

Crée un nouveau `.json` dans ce dossier en suivant le schéma documenté dans
[`aosis-deck-builder/references/json-schema.md`](../aosis-deck-builder/references/json-schema.md). Le catalogue des layouts est dans [`aosis-deck-builder/references/layouts.md`](../aosis-deck-builder/references/layouts.md).
