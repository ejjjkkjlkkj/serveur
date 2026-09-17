# Accessible Server

Serveur Windows natif pensé dès le départ pour une administration utilisable au clavier et avec NVDA, JAWS et le Narrateur.

## Architecture cible

- cœur serveur en Rust 1.98.1, edition 2024 ;
- runtime asynchrone Tokio ;
- API HTTP typée avec Axum ;
- stockage SQLite via SQLx ;
- journalisation structurée avec tracing ;
- interface d'administration Web en HTML sémantique, sans framework graphique propriétaire ;
- exécutable Windows autonome ;
- service Windows natif ;
- installateur MSI construit par GitHub Actions ;
- build release optimisé avec LTO, codegen-units=1 et panic=abort.

## Accessibilité

L'accessibilité est un gate de release, pas une option. La publication stable exige : navigation clavier complète, focus visible, structure HTML native, noms/rôles/états accessibles, messages dynamiques annoncés, compatibilité fort contraste et zoom, tests automatisés et validation manuelle NVDA/JAWS/Narrateur.

Voir [ACCESSIBILITY.md](ACCESSIBILITY.md).

## État

Initialisation du socle Rust et de la chaîne de build Windows en cours.
