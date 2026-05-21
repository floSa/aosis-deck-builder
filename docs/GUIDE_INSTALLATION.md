# Guide d'installation — aosis-deck-builder

**Comment installer le skill `aosis-deck-builder` dans tous les environnements Claude**

Ce guide couvre l'installation et la mise à jour du skill dans :
1. **Claude Code via VS Code** (ton environnement actuel)
2. **Claude Code CLI** (terminal natif)
3. **Claude Desktop** (Chat + Cowork)
4. **Claude.ai** (web)

---

## 1. Vue d'ensemble — Qu'est-ce qu'un skill Claude ?

Un skill est un **dossier contenant un fichier `SKILL.md`** avec :
- Un en-tête YAML (frontmatter) avec `name` et `description`
- Des instructions en markdown
- Optionnellement : un dossier `scripts/`, `references/`, `assets/`

Ton skill `aosis-deck-builder/` respecte déjà cette structure.

**Deux modes d'installation existent** selon le contexte :

| Contexte | Méthode | Où vit le skill |
|---|---|---|
| Claude Code (CLI ou VS Code) | Copie de dossier ou symlink | `~/.claude/skills/<nom>/` ou `.claude/skills/<nom>/` (projet) |
| Claude Desktop (Chat + Cowork) | Upload d'un fichier ZIP via l'UI | Stocké côté serveur Anthropic |
| Claude.ai (web) | Upload d'un fichier ZIP via l'UI | Stocké côté serveur Anthropic |

---

## 2. Pré-requis communs

### 2.1 — Vérifier que le skill est complet

Avant toute installation, dans WSL :

```bash
cd ~/Projets/Skill_pptx_Aosis
ls aosis-deck-builder/
```

Tu dois voir :
- `SKILL.md`
- `scripts/`
- `references/`
- `assets/`
- `tests/`
- `pyproject.toml`

### 2.2 — Vérifier le frontmatter du SKILL.md

```bash
head -10 aosis-deck-builder/SKILL.md
```

Le fichier doit commencer par un en-tête YAML du type :

```yaml
---
name: aosis-deck-builder
description: Génère des présentations PowerPoint consulting AOSIS avec layouts pré-conçus, palette et police charte, charts matplotlib, images Pexels, et compositions libres. À utiliser quand l'utilisateur demande un deck/présentation/slide PPTX dans le style AOSIS.
---
```

**Important** : si le nom contient des espaces ou majuscules, l'installation peut échouer. Le nom doit être en `kebab-case` (lettres minuscules + tirets uniquement).

### 2.3 — La clé Pexels

Le skill utilise `PEXELS_API_KEY` chargée depuis un fichier `.env`. Selon le contexte d'installation :

- **Claude Code** : la clé est lue depuis `.env` à la racine du projet (déjà configuré)
- **Claude Desktop / Claude.ai** : la clé devra être fournie autrement (variable d'environnement côté serveur OU le skill devra gérer l'absence gracieusement avec fallback Picsum)

À noter : sur Claude Desktop/web, l'environnement d'exécution est différent (sandbox Anthropic) et il faut vérifier si la lecture du `.env` fonctionne ou non. Le fallback Picsum garantit que le skill ne plante pas.

---

## 3. Installation dans Claude Code (CLI + VS Code)

Claude Code utilise des dossiers locaux pour découvrir les skills. C'est ton environnement actuel.

### 3.1 — Installation personnelle (recommandée pour usage quotidien)

Skills disponibles dans tous tes projets sur cette machine. Stockés dans `~/.claude/skills/`.

```bash
# Créer le dossier si pas existant
mkdir -p ~/.claude/skills

# Copier ton skill (ou créer un symlink pour rester sync avec ton repo)
# Option A : copie simple
cp -r ~/Projets/Skill_pptx_Aosis/aosis-deck-builder ~/.claude/skills/aosis-deck-builder

# Option B (recommandée pour le développement) : symlink
# Ainsi toute modification dans ton repo est immédiatement vue par Claude Code
ln -s ~/Projets/Skill_pptx_Aosis/aosis-deck-builder ~/.claude/skills/aosis-deck-builder
```

**Vérification** :
```bash
ls -la ~/.claude/skills/
```

Tu dois voir `aosis-deck-builder` listé.

### 3.2 — Installation projet (pour équipe)

Skills disponibles uniquement dans un projet précis, partageable via Git. Stockés dans `.claude/skills/` à la racine du projet.

```bash
cd /chemin/vers/mon-projet-client
mkdir -p .claude/skills
ln -s ~/Projets/Skill_pptx_Aosis/aosis-deck-builder .claude/skills/aosis-deck-builder

# Optionnel : commit pour partager avec ton équipe
git add .claude/skills/aosis-deck-builder
git commit -m "Ajout skill aosis-deck-builder pour la génération de decks"
```

**Note** : pour partager via Git, il faut soit committer le contenu réel (pas le symlink), soit utiliser un submodule Git. Le symlink ne fonctionnera pas pour les autres membres de l'équipe.

### 3.3 — Activation et test

1. **Ferme et relance Claude Code** (ou recharge la fenêtre VS Code)
2. Dans une session Claude Code, teste :
   ```
   Quels skills as-tu disponibles ?
   ```
   Tu dois voir `aosis-deck-builder` dans la liste.
3. Pour invoquer le skill explicitement :
   ```
   Utilise le skill aosis-deck-builder pour générer un deck à partir de ce brief : ...
   ```

### 3.4 — Mise à jour du skill

Si tu as utilisé un **symlink**, aucune action : tes modifications dans `~/Projets/Skill_pptx_Aosis/aosis-deck-builder/` sont immédiatement reflétées.

Si tu as utilisé une **copie**, refais la copie :
```bash
rm -rf ~/.claude/skills/aosis-deck-builder
cp -r ~/Projets/Skill_pptx_Aosis/aosis-deck-builder ~/.claude/skills/aosis-deck-builder
```

### 3.5 — Désinstallation

```bash
# Personal
rm -rf ~/.claude/skills/aosis-deck-builder

# Projet
rm -rf .claude/skills/aosis-deck-builder
```

Ou pour désactiver temporairement sans supprimer :
```bash
mv ~/.claude/skills/aosis-deck-builder ~/.claude/skills/_aosis-deck-builder
```
Le préfixe underscore fait que Claude ne charge plus le skill. Renomme sans underscore pour réactiver.

---

## 4. Installation dans Claude Desktop (Chat + Cowork)

Claude Desktop est l'application de bureau Anthropic (Mac/Windows/Linux) qui contient Chat, Cowork et Code dans une même interface. L'installation des skills se fait via une **upload ZIP**.

### 4.1 — Préparer le ZIP

Le ZIP doit contenir un **dossier** qui contient le `SKILL.md` et ses dépendances.

```bash
cd ~/Projets/Skill_pptx_Aosis
zip -r aosis-deck-builder.zip aosis-deck-builder/ \
  -x "aosis-deck-builder/__pycache__/*" \
  -x "aosis-deck-builder/.pytest_cache/*" \
  -x "aosis-deck-builder/tests/__pycache__/*"
```

**Vérifications avant upload** :
- Le ZIP doit faire moins de 50 Mo (limite Anthropic)
- Le fichier `SKILL.md` doit avoir un frontmatter YAML valide
- Pas de symlinks dans le ZIP

```bash
unzip -l aosis-deck-builder.zip | head -20
# Doit montrer aosis-deck-builder/ comme dossier racine + SKILL.md à l'intérieur
```

### 4.2 — Activer la fonctionnalité Skills

Avant d'uploader, active "Code execution and file creation" dans tes paramètres Claude :

1. Ouvre **Claude Desktop**
2. Clique sur ton avatar (en bas à gauche)
3. Va dans **Settings** → **Capabilities**
4. Active **"Code execution and file creation"**

Sans cette option, les skills ne peuvent pas exécuter de scripts Python.

### 4.3 — Uploader le skill

1. Dans Claude Desktop, ouvre la sidebar gauche
2. Clique sur **Customize**
3. Sélectionne **Skills**
4. Clique sur le bouton **+**
5. Choisis **Upload a skill**
6. Sélectionne ton `aosis-deck-builder.zip`
7. Confirme l'upload (quelques secondes)
8. Le skill apparaît dans ta liste de skills avec un toggle pour l'activer

### 4.4 — Utilisation dans Chat

Une fois activé, le skill se charge **automatiquement** quand tu demandes quelque chose qui matche sa description.

Exemple :
```
Génère-moi un deck consulting AOSIS sur la migration cloud
de l'entreprise TechnoLog. Voici le brief : ...
```

Claude détecte le besoin de génération de deck PPTX → charge le skill `aosis-deck-builder` → exécute le workflow.

### 4.5 — Utilisation dans Cowork

Cowork permet des tâches asynchrones / longues. Pour invoquer le skill :

1. Dans Cowork, tape `/` dans la zone de chat
2. Une liste de tes skills apparaît
3. Sélectionne `aosis-deck-builder`
4. Décris ta tâche
5. Cowork lance la génération en arrière-plan

### 4.6 — Limite importante pour Cloud Code via Desktop

Le skill `aosis-deck-builder` exécute des scripts Python qui dépendent de :
- `python-pptx`
- `matplotlib`
- `Pillow`
- L'environnement WSL Ubuntu (chemins, polices Arial, etc.)

Sur **Claude Desktop**, l'exécution se fait dans un **sandbox Anthropic** qui peut ou non avoir ces dépendances. Le mieux est de tester :

1. Upload le skill
2. Lance une génération test
3. Si erreur de dépendances, soit :
   - Ajouter un `requirements.txt` ou `pyproject.toml` au skill
   - Modifier le `SKILL.md` pour qu'il installe les dépendances au démarrage (`pip install python-pptx matplotlib pillow`)
   - Utiliser le skill uniquement via Claude Code (où l'environnement WSL est sous ton contrôle)

**Recommandation** : pour l'instant, **garde Claude Code comme environnement principal** pour ce skill. Claude Desktop fonctionnera pour des usages plus simples.

### 4.7 — Mise à jour du skill dans Claude Desktop

1. Recréer le ZIP avec la nouvelle version
2. Dans Claude Desktop → Customize → Skills
3. Clique sur ton skill existant
4. Bouton **Replace** ou **Update** (selon version de l'UI)
5. Upload le nouveau ZIP

Si pas de bouton de remplacement : supprimer l'ancien skill et uploader le nouveau.

---

## 5. Installation dans Claude.ai (web)

L'interface web utilise le même mécanisme que Claude Desktop pour les skills.

### 5.1 — Activer la fonctionnalité

1. Va sur **claude.ai**
2. Clique sur ton avatar (en bas à gauche)
3. **Settings** → **Capabilities**
4. Active **"Code execution and file creation"**

### 5.2 — Uploader le skill

1. Dans la sidebar gauche, clique sur **Customize**
2. Sélectionne **Skills**
3. Clique sur **+**
4. Upload **a skill**
5. Sélectionne `aosis-deck-builder.zip`

Le skill est partagé entre Claude Desktop et Claude.ai (web) si tu utilises le même compte. Pas besoin de l'uploader deux fois.

### 5.3 — Limitations identiques

Même remarque que pour Claude Desktop : l'environnement d'exécution est un sandbox Anthropic, les dépendances Python doivent être disponibles ou installées par le skill.

---

## 6. Partage avec ton équipe AOSIS

### 6.1 — Plan Team / Enterprise (recommandé)

Si AOSIS a un plan Team ou Enterprise Claude :

1. Owner du compte va dans **Organization settings** → **Skills**
2. Active **"Skill sharing"** et **"Share with organization"**
3. Toi : dans **Customize** → **Skills**, clique sur ton skill
4. Bouton **Share** → choisis l'organisation ou des personnes précises
5. Tes collègues voient le skill dans leur section **Shared with you**

### 6.2 — Partage manuel (plan individuel)

1. Envoie le `aosis-deck-builder.zip` par email/Slack
2. Chaque collègue suit la procédure d'upload (section 4 ou 5)

### 6.3 — Partage via Git (Claude Code uniquement)

Pour partager dans un repo Git :

1. Mets le dossier `aosis-deck-builder/` dans ton repo (sans symlink)
2. Documente dans le README la commande d'installation locale :
   ```bash
   ln -s $(pwd)/aosis-deck-builder ~/.claude/skills/aosis-deck-builder
   ```
3. Chaque dev clone le repo et exécute la commande

---

## 7. Vérification et tests post-installation

### 7.1 — Test rapide dans Claude Code

```
Liste les skills que tu as disponibles dans le projet courant.
```

Tu dois voir `aosis-deck-builder` mentionné.

### 7.2 — Test fonctionnel

```
Utilise le skill aosis-deck-builder pour générer un deck test de 3 slides
sur le thème "Migration vers le cloud". Garde-le simple : une cover,
une slide de contenu avec 3 KPI, et une slide de clôture.
```

Claude doit :
1. Lire le `SKILL.md`
2. Proposer un plan
3. Générer un JSON spec
4. Lancer `build_deck.py`
5. Te livrer un `.pptx`

### 7.3 — Diagnostic en cas de problème

**Le skill n'apparaît pas** :
- Vérifie le chemin : `ls ~/.claude/skills/`
- Vérifie le frontmatter du `SKILL.md`
- Relance Claude Code
- Vérifie le nom (kebab-case obligatoire)

**Le skill apparaît mais ne se charge pas** :
- La description est peut-être trop vague (Claude ne sait pas quand l'utiliser)
- Améliore la description dans le frontmatter pour qu'elle mentionne les mots-clés déclencheurs ("PowerPoint", "deck", "présentation", "AOSIS", "consulting", "pptx")

**Le skill se charge mais plante à l'exécution** :
- Vérifie que les dépendances Python sont installées dans l'environnement courant
- Vérifie que `PEXELS_API_KEY` est accessible
- Vérifie que `AOSIS_template.pptx` est bien dans `assets/`

---

## 8. Récapitulatif par environnement

| Environnement | Méthode | Chemin / lieu | Commande type |
|---|---|---|---|
| Claude Code CLI (perso) | Copie ou symlink | `~/.claude/skills/aosis-deck-builder/` | `ln -s $(pwd)/aosis-deck-builder ~/.claude/skills/` |
| Claude Code CLI (projet) | Copie ou symlink | `.claude/skills/aosis-deck-builder/` | `ln -s ~/Projets/.../aosis-deck-builder .claude/skills/` |
| Claude Code via VS Code | Identique au CLI | Identique | Identique |
| Claude Desktop (Chat) | Upload ZIP | UI Settings | Settings → Skills → Upload |
| Claude Desktop (Cowork) | Auto via Chat | UI partagée | Identique au Chat |
| Claude.ai (web) | Upload ZIP | UI Settings | Identique Desktop |

---

## 9. Recommandation pour ton usage AOSIS

D'après ton workflow actuel :

1. **Garde Claude Code dans VS Code comme environnement principal** pour la génération de decks (env Python contrôlé, clé Pexels via `.env`, scripts complexes qui marchent).

2. **Installe le skill en symlink personnel** :
   ```bash
   ln -s ~/Projets/Skill_pptx_Aosis/aosis-deck-builder ~/.claude/skills/aosis-deck-builder
   ```
   Avantage : toute modification de ton skill est immédiate.

3. **Uploade aussi le ZIP dans Claude Desktop** pour avoir le skill disponible côté Chat/Cowork quand tu fais des tâches plus simples (pas de génération PPTX complexe, juste des conseils sur le contenu d'un deck par exemple).

4. **Partage avec ton équipe AOSIS** uniquement quand tu auras validé le skill sur 2-3 vrais cas client. Évite de partager une V1 buggée qui ferait perdre confiance.

5. **Documentation** : le `SKILL.md` doit avoir une description très précise des cas d'usage déclencheurs. C'est ce qui fait que Claude charge ou non le skill au bon moment.

---

## 10. Améliorations futures du SKILL.md

Pour optimiser le déclenchement automatique du skill dans Chat/Cowork, vérifie que ton frontmatter contient des mots-clés explicites :

```yaml
---
name: aosis-deck-builder
description: |
  Génère des présentations PowerPoint au format consulting AOSIS.
  À utiliser quand l'utilisateur demande :
  - Un deck, une présentation, un PowerPoint, un PPTX
  - Une slide AOSIS, un slide de pitch, un deck consulting
  - La restitution d'un audit, brief, rapport en présentation
  - Une mise en forme visuelle d'analyse, recommandation, plan
  Couvre les layouts : cover, agenda, sections, KPIs, charts, tableaux,
  matrices 2x2, roadmaps, citations, compositions libres canvas_blank.
  Inclut palette AOSIS automatique, police Arial, images Pexels, charts matplotlib.
---
```

Plus la description couvre de variantes ("deck", "présentation", "slides", "PPTX", "consulting", "pitch"), plus Claude est susceptible de charger le skill au bon moment.

---

## 11. Sources officielles

Pour aller plus loin :

- **Documentation Anthropic Claude Code** : https://code.claude.com/docs/en/skills
- **Help Center — Use Skills in Claude** : https://support.claude.com/en/articles/12512180-use-skills-in-claude
- **Help Center — Plugins in Cowork** : https://support.claude.com/en/articles/13837440-use-plugins-in-claude-cowork

---

**Fin du guide d'installation. À jour avec les mécanismes Claude en mai 2026.**
