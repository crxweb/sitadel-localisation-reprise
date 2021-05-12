UPDATE frontend_localisation loc
INNER JOIN frontend_localisation_villes_reprise vr on vr.ville_id = loc.localisation_villeId AND vr.ville_newId IS NOT NULL
SET loc.localisation_villeId = vr.ville_newId;