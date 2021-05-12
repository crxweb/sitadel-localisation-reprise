--
-- Table structure for table `frontend_localisation_departements`
--

CREATE TABLE `frontend_localisation_departements` (
  `departement_id` int(11) NOT NULL,
  `departement_DEP` varchar(3) NOT NULL DEFAULT '',
  `departement_REG` varchar(2) NOT NULL DEFAULT '',
  `departement_CHEFLIEU` varchar(5) NOT NULL DEFAULT '',
  `departement_TNCC` int(1) NOT NULL DEFAULT '0',
  `departement_NCC` varchar(200) NOT NULL DEFAULT '',
  `departement_NCCENR` varchar(200) NOT NULL DEFAULT '',
  `departement_LIBELLE` varchar(200) NOT NULL DEFAULT '',
  `departement_dateAdded` datetime DEFAULT NULL,
  `departement_dateUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Départements au 01/01/2021 - INSEE Code Officiel Géographique';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `frontend_localisation_departements`
--
ALTER TABLE `frontend_localisation_departements`
  ADD PRIMARY KEY (`departement_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `frontend_localisation_departements`
--
ALTER TABLE `frontend_localisation_departements`
  MODIFY `departement_id` int(11) NOT NULL AUTO_INCREMENT;
