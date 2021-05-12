--
-- Table structure for table `frontend_localisation_regions`
--

CREATE TABLE `frontend_localisation_regions` (
  `region_id` int(11) NOT NULL,
  `region_REG` varchar(2) NOT NULL DEFAULT '',
  `region_CHEFLIEU` varchar(5) NOT NULL DEFAULT '',
  `region_TNCC` int(1) NOT NULL DEFAULT '0',
  `region_NCC` varchar(200) NOT NULL DEFAULT '',
  `region_NCCENR` varchar(200) NOT NULL DEFAULT '',
  `region_LIBELLE` varchar(200) NOT NULL DEFAULT '',
  `region_dateAdded` datetime DEFAULT NULL,
  `region_dateUpdated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Régions au 01/01/2021 - INSEE Code Officiel Géographique';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `frontend_localisation_regions`
--
ALTER TABLE `frontend_localisation_regions`
  ADD PRIMARY KEY (`region_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `frontend_localisation_regions`
--
ALTER TABLE `frontend_localisation_regions`
  MODIFY `region_id` int(11) NOT NULL AUTO_INCREMENT;
