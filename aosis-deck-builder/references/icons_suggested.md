# Icônes consulting recommandées

Le champ `icons` du JSON spec accepte des identifiants [Iconify](https://icon-sets.iconify.design/)
au format `<prefix>:<name>`. Plus de 200 000 icônes disponibles via 150+ libraries open-source.

Le moteur télécharge automatiquement l'icône depuis l'API Iconify (`api.iconify.design`),
applique la couleur navy AOSIS, et l'insère par-dessus la shape `{{ITEM_ICON}}` du layout.

**Si l'API est inaccessible** (réseau coupé, timeout, identifiant invalide) : le moteur
continue silencieusement sans icône. Pas d'erreur bloquante.

## Identifiants recommandés par contexte

### Stratégie & Vision
- `mdi:lightbulb` — idée, vision
- `mdi:target` — cible, objectif
- `mdi:compass` — direction, stratégie
- `material-symbols:rocket-launch` — lancement, ambition
- `mdi:eye` — vision, prospective

### Cloud & Infrastructure
- `mdi:cloud` — cloud public
- `mdi:cloud-upload` — migration vers le cloud
- `mdi:server` — datacenter, on-premise
- `mdi:server-network` — infrastructure réseau
- `carbon:edge-cluster` — edge computing
- `mdi:database` — base de données, stockage
- `mdi:kubernetes` — containers, orchestration

### Data & Analytics
- `mdi:chart-line` — performance, tendance
- `mdi:chart-bar` — analytics, KPI
- `carbon:data-vis-1` — data visualization
- `mdi:database-search` — exploration data
- `mdi:graphql` — API, intégration data
- `material-symbols:analytics` — analyse

### Sécurité & Gouvernance
- `mdi:shield-check` — sécurité validée
- `mdi:shield-lock` — confidentialité
- `mdi:lock` — accès restreint
- `mdi:account-key` — IAM, authentification
- `mdi:gavel` — gouvernance, conformité
- `carbon:policy` — règles, politique
- `mdi:certificate` — certification

### Performance & Optimisation
- `mdi:speedometer` — performance
- `mdi:rocket` — accélération
- `mdi:arrow-up-bold` — croissance
- `mdi:cog-sync` — automatisation
- `material-symbols:bolt` — vélocité, agilité
- `mdi:trending-up` — progression

### Équipe & Organisation
- `mdi:account-group` — équipe
- `mdi:account-tie` — sponsor, dirigeant
- `mdi:school` — formation, upskilling
- `mdi:handshake` — partenariat
- `mdi:account-supervisor` — leadership
- `material-symbols:groups` — collaboration

### Temps & Roadmap
- `mdi:clock-outline` — délai
- `mdi:calendar-clock` — planning
- `mdi:flag` — milestone, jalon
- `mdi:road-variant` — roadmap, parcours
- `material-symbols:schedule` — calendrier

### Argent & Business
- `mdi:cash` — coût, TCO
- `mdi:currency-eur` — montant en euros
- `mdi:trending-down` — réduction coût
- `mdi:scale-balance` — ROI, équilibre
- `mdi:bank` — finance, trésorerie

### Risque & Alerte
- `mdi:alert-circle` — risque identifié
- `mdi:alert-octagon` — risque critique
- `mdi:shield-alert` — vulnérabilité
- `mdi:fire` — urgence
- `mdi:weather-cloudy-alert` — incident cloud

### Process & Méthode
- `mdi:cog` — engrenage, méthode
- `mdi:tools` — outillage, technique
- `mdi:source-branch` — git, versioning
- `mdi:sync` — itération, agile
- `material-symbols:settings` — configuration
- `mdi:flow-line` — process

## Pattern d'usage dans le JSON spec

```json
{
  "layout": "framework_3cards",
  "title": "Les 3 piliers du succès",
  "icons": ["mdi:account-tie", "mdi:school", "mdi:tools"],
  "items": [
    {"title": "Sponsorship", "bullets": "..."},
    {"title": "Compétences", "bullets": "..."},
    {"title": "Méthode",     "bullets": "..."}
  ]
}
```

L'ordre du tableau `icons` correspond à l'ordre des `items`. Pour omettre une icône
sur un item particulier, passer `null` ou une chaîne vide à la position correspondante.

## Comment chercher une icône

1. Naviguer [icon-sets.iconify.design](https://icon-sets.iconify.design/)
2. Chercher par mot-clé (en anglais de préférence : "cloud", "security", "rocket")
3. Copier l'identifiant complet affiché sous l'icône (ex: `material-symbols:rocket-launch`)
4. Le coller dans le tableau `icons` du spec

## Préférences AOSIS

- Privilégier les libraries **Material Design Icons** (`mdi:*`) et **Material Symbols**
  (`material-symbols:*`) pour la cohérence graphique avec PowerPoint.
- Éviter les icônes trop détaillées ou colorées d'origine (elles seront recolorées en
  navy mais peuvent perdre en lisibilité).
- Tester systématiquement le rendu : certaines icônes ont un trait fin qui s'efface
  à petite taille.
