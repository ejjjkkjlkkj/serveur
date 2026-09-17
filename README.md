# Accessible Server

Serveur Windows pensé dès le départ pour une administration utilisable au clavier et avec NVDA, JAWS et le Narrateur.

## Objectif

Le produit suit une architecture simple et robuste :

- moteur serveur HTTP/API en Python ;
- interface d’administration Web en HTML sémantique, utilisable sans souris ;
- API JSON pour l’automatisation ;
- stockage local SQLite sans dépendance serveur externe ;
- exécutable Windows autonome ;
- installateur MSI construit automatiquement par GitHub Actions.

## Accessibilité

Les critères de release incluent : navigation clavier complète, ordre de lecture logique, titres et zones structurées, noms accessibles explicites, absence de dépendance à la couleur, focus visible et tests avec lecteurs d’écran.

## État

Initialisation du projet et de la chaîne de build Windows.
