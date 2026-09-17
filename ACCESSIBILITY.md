# Politique d'accessibilité

L'accessibilité est un critère bloquant de release pour Accessible Server.

## Cible

L'administration doit être utilisable sans souris avec :

- NVDA sous Windows ;
- JAWS sous Windows ;
- Narrateur Windows ;
- navigation clavier seule ;
- zoom et fort contraste Windows ;
- navigateur en mode couleurs forcées.

## Référence NVDA portable

La référence NVDA principale pour les validations Windows est l'archive locale fournie pour le projet :

- produit : NVDA 2026.2 ;
- FileVersion : `2026.2.0.57664` ;
- ProductVersion : `2026.2` ;
- exécutables présents : `NVDA/nvda.exe` et `NVDA/nvda_noUIAccess.exe` ;
- SHA-256 de l'archive de référence : `ab23a489c9e3d4310856fd8e77a63bb5b20d089077ec95d55d56fffac2c891fd`.

Le binaire NVDA n'est pas versionné dans ce dépôt. Les tests doivent utiliser une copie locale isolée de cette archive, avec une configuration NVDA dédiée aux tests afin de ne pas dépendre du profil utilisateur.

## Règles d'interface

- HTML natif et sémantique en priorité ;
- un seul `h1`, hiérarchie de titres cohérente ;
- zones `header`, `nav`, `main`, `footer` ;
- lien d'évitement vers le contenu principal ;
- tous les contrôles utilisables avec Tab, Maj+Tab, Entrée et Espace selon leur sémantique ;
- aucun gestionnaire de clic sur des éléments non interactifs ;
- focus clavier toujours visible ;
- ordre de focus identique à l'ordre logique du DOM ;
- noms, rôles, états et valeurs accessibles explicites ;
- messages d'état importants annoncés via une zone live appropriée ;
- tableaux avec `caption` et en-têtes associés ;
- erreurs textuelles, jamais indiquées uniquement par une couleur ;
- interface utilisable à 200 % de zoom ;
- aucun contenu essentiel dépendant d'une animation ;
- prise en charge de `prefers-reduced-motion` et `forced-colors` ;
- contraste conforme WCAG 2.2 AA au minimum.

## Gates automatisés

Une release doit passer :

1. compilation Rust sans avertissements bloquants ;
2. `cargo fmt --check` ;
3. `cargo clippy` ;
4. tests unitaires et d'intégration ;
5. audit des dépendances ;
6. tests HTTP de santé ;
7. analyse automatisée d'accessibilité de l'interface ;
8. vérification que les contrôles sont atteignables au clavier.

## Validation lecteurs d'écran

Avant une release stable, exécuter au minimum cette matrice sur Windows :

| Test | NVDA | JAWS | Narrateur |
|---|---|---|---|
| Lecture du titre de page | requis | requis | requis |
| Navigation par titres | requis | requis | requis |
| Navigation par régions | requis | requis | requis |
| Navigation Tab/Maj+Tab | requis | requis | requis |
| Activation des liens/boutons | requis | requis | requis |
| Lecture du statut serveur | requis | requis | requis |
| Lecture du tableau d'événements | requis | requis | requis |
| Annonce des mises à jour dynamiques | requis | requis | requis |
| Zoom 200 % | requis | requis | requis |
| Contraste élevé / couleurs forcées | requis | requis | requis |

Toute régression sérieuse ou critique bloque la publication du MSI et de l'EXE de release.
