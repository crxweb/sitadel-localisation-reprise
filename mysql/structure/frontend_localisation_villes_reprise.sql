--
-- Table structure for table `frontend_localisation_villes_reprise`
--

CREATE TABLE `frontend_localisation_villes_reprise` (
  `ville_id` int(11) NOT NULL,
  `ville_INSEE` varchar(7) NOT NULL DEFAULT '',
  `ville_CDC` varchar(255) DEFAULT NULL,
  `ville_CHEFLIEU` varchar(255) DEFAULT NULL,
  `ville_REG` varchar(255) DEFAULT NULL,
  `ville_DEP` varchar(255) DEFAULT NULL,
  `ville_COM` varchar(255) DEFAULT NULL,
  `ville_AR` varchar(255) DEFAULT NULL,
  `ville_CT` varchar(255) DEFAULT NULL,
  `ville_TNCC` varchar(255) DEFAULT NULL,
  `ville_ARTMAJ` varchar(255) DEFAULT NULL,
  `ville_NCC` varchar(255) DEFAULT NULL,
  `ville_ARTMIN` varchar(255) DEFAULT NULL,
  `ville_NCCENR` varchar(255) DEFAULT NULL,
  `ville_LAT` float(10,7) DEFAULT NULL,
  `ville_LONG` float(10,7) DEFAULT NULL,
  `ville_CP` varchar(35) DEFAULT NULL,
  `ville_dateAdded` datetime DEFAULT NULL,
  `ville_dateUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ville_newId` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `frontend_localisation_villes_reprise`
--
ALTER TABLE `frontend_localisation_villes_reprise`
  ADD PRIMARY KEY (`ville_id`),
  ADD UNIQUE KEY `INSEE` (`ville_INSEE`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `frontend_localisation_villes_reprise`
--
ALTER TABLE `frontend_localisation_villes_reprise`
  MODIFY `ville_id` int(11) NOT NULL AUTO_INCREMENT;