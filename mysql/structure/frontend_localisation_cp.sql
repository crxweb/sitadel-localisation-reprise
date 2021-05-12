--
-- Table structure for table `frontend_localisation_cp`
--

CREATE TABLE `frontend_localisation_cp` (
  `cp_id` int(11) NOT NULL,
  `cp_Code_commune_INSEE` varchar(5) NOT NULL DEFAULT '',
  `cp_Nom_commune` varchar(255) NOT NULL DEFAULT '',
  `cp_Code_postal` varchar(5) NOT NULL DEFAULT '',
  `cp_Ligne_5` varchar(255) DEFAULT NULL,
  `cp_Libelle_d_acheminement` varchar(255) NOT NULL DEFAULT '',
  `cp_lat` float(10,7) DEFAULT NULL,
  `cp_lng` float(10,7) DEFAULT NULL,
  `cp_dateAdded` datetime DEFAULT NULL,
  `cp_dateUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Correspondance entre codes postaux et codes INSEE communes - Laposte';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `frontend_localisation_cp`
--
ALTER TABLE `frontend_localisation_cp`
  ADD PRIMARY KEY (`cp_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `frontend_localisation_cp`
--
ALTER TABLE `frontend_localisation_cp`
  MODIFY `cp_id` int(11) NOT NULL AUTO_INCREMENT;
