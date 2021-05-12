--
-- Table structure for table `frontend_localisation_villes`
--

CREATE TABLE `frontend_localisation_villes` (
  `ville_id` int(11) NOT NULL,
  `ville_TYPECOM` varchar(4) NOT NULL DEFAULT '',
  `ville_COM` varchar(5) NOT NULL DEFAULT '',
  `ville_REG` varchar(2) DEFAULT NULL,
  `ville_DEP` varchar(3) DEFAULT NULL,
  `ville_CTCD` varchar(4) DEFAULT NULL,
  `ville_ARR` varchar(4) DEFAULT NULL,
  `ville_TNCC` int(1) NOT NULL DEFAULT '0',
  `ville_NCC` varchar(200) NOT NULL DEFAULT '',
  `ville_NCCENR` varchar(200) NOT NULL DEFAULT '',
  `ville_LIBELLE` varchar(200) NOT NULL DEFAULT '',
  `ville_CAN` varchar(5) DEFAULT NULL,
  `ville_COMPARENT` varchar(5) DEFAULT NULL,
  `ville_dateAdded` datetime DEFAULT NULL,
  `ville_dateUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Communes au 01/01/2021 - INSEE Code Officiel Géographique';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `frontend_localisation_villes`
--
ALTER TABLE `frontend_localisation_villes`
  ADD PRIMARY KEY (`ville_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `frontend_localisation_villes`
--
ALTER TABLE `frontend_localisation_villes`
  MODIFY `ville_id` int(11) NOT NULL AUTO_INCREMENT;
