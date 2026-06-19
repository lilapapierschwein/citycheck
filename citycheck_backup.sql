PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE continents (
	continent_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (continent_id), 
	UNIQUE (name)
);
INSERT INTO continents VALUES(1,'Africa');
INSERT INTO continents VALUES(2,'Antarctica');
INSERT INTO continents VALUES(3,'Asia');
INSERT INTO continents VALUES(4,'Europe');
INSERT INTO continents VALUES(5,'North America');
INSERT INTO continents VALUES(6,'Oceania');
INSERT INTO continents VALUES(7,'South America');
CREATE TABLE regions (
	region_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (region_id), 
	UNIQUE (name)
);
INSERT INTO regions VALUES(1,'Africa');
INSERT INTO regions VALUES(2,'Americas');
INSERT INTO regions VALUES(3,'Antarctic');
INSERT INTO regions VALUES(4,'Asia');
INSERT INTO regions VALUES(5,'Europe');
INSERT INTO regions VALUES(6,'Oceania');
CREATE TABLE languages (
	language_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (language_id), 
	UNIQUE (name)
);
INSERT INTO languages VALUES(1,'Abkhaz');
INSERT INTO languages VALUES(2,'Afrikaans');
INSERT INTO languages VALUES(3,'Albanian');
INSERT INTO languages VALUES(4,'Amharic');
INSERT INTO languages VALUES(5,'Arabic');
INSERT INTO languages VALUES(6,'Aramaic');
INSERT INTO languages VALUES(7,'Aranese');
INSERT INTO languages VALUES(8,'Armenian');
INSERT INTO languages VALUES(9,'Aymara');
INSERT INTO languages VALUES(10,'Azerbaijani');
INSERT INTO languages VALUES(11,'Barwe');
INSERT INTO languages VALUES(12,'Basque');
INSERT INTO languages VALUES(13,'Belarusian');
INSERT INTO languages VALUES(14,'Belize Kriol');
INSERT INTO languages VALUES(15,'Bengali');
INSERT INTO languages VALUES(16,'Bislama');
INSERT INTO languages VALUES(17,'Bosnian');
INSERT INTO languages VALUES(18,'Bulgarian');
INSERT INTO languages VALUES(19,'Burmese');
INSERT INTO languages VALUES(20,'Carolinian');
INSERT INTO languages VALUES(21,'Catalan');
INSERT INTO languages VALUES(22,'Central Kurdish');
INSERT INTO languages VALUES(23,'Chamorro');
INSERT INTO languages VALUES(24,'Chichewa');
INSERT INTO languages VALUES(25,'Chinese');
INSERT INTO languages VALUES(26,'Cook Islands Maori');
INSERT INTO languages VALUES(27,'Croatian');
INSERT INTO languages VALUES(28,'Czech');
INSERT INTO languages VALUES(29,'Danish');
INSERT INTO languages VALUES(30,'Dari');
INSERT INTO languages VALUES(31,'Divehi');
INSERT INTO languages VALUES(32,'Dutch');
INSERT INTO languages VALUES(33,'Dzongkha');
INSERT INTO languages VALUES(34,'English');
INSERT INTO languages VALUES(35,'Estonian');
INSERT INTO languages VALUES(36,'Faroese');
INSERT INTO languages VALUES(37,'Fiji Hindi');
INSERT INTO languages VALUES(38,'Fijian');
INSERT INTO languages VALUES(39,'Filipino');
INSERT INTO languages VALUES(40,'Finnish');
INSERT INTO languages VALUES(41,'French');
INSERT INTO languages VALUES(42,'Galician');
INSERT INTO languages VALUES(43,'Georgian');
INSERT INTO languages VALUES(44,'German');
INSERT INTO languages VALUES(45,'Gilbertese');
INSERT INTO languages VALUES(46,'Greek');
INSERT INTO languages VALUES(47,'Greenlandic');
INSERT INTO languages VALUES(48,'Guarani');
INSERT INTO languages VALUES(49,'Haitian Creole');
INSERT INTO languages VALUES(50,'Hai‖om');
INSERT INTO languages VALUES(51,'Hassaniya Arabic');
INSERT INTO languages VALUES(52,'Hebrew');
INSERT INTO languages VALUES(53,'Herero');
INSERT INTO languages VALUES(54,'Hindi');
INSERT INTO languages VALUES(55,'Hiri Motu');
INSERT INTO languages VALUES(56,'Hungarian');
INSERT INTO languages VALUES(57,'Icelandic');
INSERT INTO languages VALUES(58,'Indonesian');
INSERT INTO languages VALUES(59,'Irish');
INSERT INTO languages VALUES(60,'Italian');
INSERT INTO languages VALUES(61,'Jamaican Patois');
INSERT INTO languages VALUES(62,'Japanese');
INSERT INTO languages VALUES(63,'Kalanga');
INSERT INTO languages VALUES(64,'Kazakh');
INSERT INTO languages VALUES(65,'Khmer');
INSERT INTO languages VALUES(66,'Khoisan languages');
INSERT INTO languages VALUES(67,'Kinyarwanda');
INSERT INTO languages VALUES(68,'Kongo');
INSERT INTO languages VALUES(69,'Korean');
INSERT INTO languages VALUES(70,'Kwangali');
INSERT INTO languages VALUES(71,'Kyrgyz');
INSERT INTO languages VALUES(72,'Lao');
INSERT INTO languages VALUES(73,'Latin');
INSERT INTO languages VALUES(74,'Latvian');
INSERT INTO languages VALUES(75,'Lingala');
INSERT INTO languages VALUES(76,'Lithuanian');
INSERT INTO languages VALUES(77,'Lozi');
INSERT INTO languages VALUES(78,'Luba-Lulua');
INSERT INTO languages VALUES(79,'Lule Sami');
INSERT INTO languages VALUES(80,'Luxembourgish');
INSERT INTO languages VALUES(81,'Macedonian');
INSERT INTO languages VALUES(82,'Malagasy');
INSERT INTO languages VALUES(83,'Malay');
INSERT INTO languages VALUES(84,'Maltese');
INSERT INTO languages VALUES(85,'Manx');
INSERT INTO languages VALUES(86,'Maori');
INSERT INTO languages VALUES(87,'Marshallese');
INSERT INTO languages VALUES(88,'Mauritian Creole');
INSERT INTO languages VALUES(89,'Mongolian');
INSERT INTO languages VALUES(90,'Montenegrin');
INSERT INTO languages VALUES(91,'Nauruan');
INSERT INTO languages VALUES(92,'Ndau');
INSERT INTO languages VALUES(93,'Ndonga');
INSERT INTO languages VALUES(94,'Nepali');
INSERT INTO languages VALUES(95,'New Zealand Sign Language');
INSERT INTO languages VALUES(96,'Ngazidja Comorian');
INSERT INTO languages VALUES(97,'Niuean');
INSERT INTO languages VALUES(98,'Norfuk');
INSERT INTO languages VALUES(99,'Norman');
INSERT INTO languages VALUES(100,'Northern Ndebele');
INSERT INTO languages VALUES(101,'Northern Sami');
INSERT INTO languages VALUES(102,'Northern Sotho');
INSERT INTO languages VALUES(103,'Norwegian');
INSERT INTO languages VALUES(104,'Norwegian Bokmål');
INSERT INTO languages VALUES(105,'Norwegian Nynorsk');
INSERT INTO languages VALUES(106,'Ossetic');
INSERT INTO languages VALUES(107,'Palauan');
INSERT INTO languages VALUES(108,'Papiamento');
INSERT INTO languages VALUES(109,'Pashto');
INSERT INTO languages VALUES(110,'Persian');
INSERT INTO languages VALUES(111,'Polish');
INSERT INTO languages VALUES(112,'Portuguese');
INSERT INTO languages VALUES(113,'Quechua');
INSERT INTO languages VALUES(114,'Romanian');
INSERT INTO languages VALUES(115,'Romansh');
INSERT INTO languages VALUES(116,'Rundi');
INSERT INTO languages VALUES(117,'Russian');
INSERT INTO languages VALUES(118,'Samoan');
INSERT INTO languages VALUES(119,'Sango');
INSERT INTO languages VALUES(120,'Serbian');
INSERT INTO languages VALUES(121,'Seychellois Creole');
INSERT INTO languages VALUES(122,'Shona');
INSERT INTO languages VALUES(123,'Sinhala');
INSERT INTO languages VALUES(124,'Slovak');
INSERT INTO languages VALUES(125,'Slovenian');
INSERT INTO languages VALUES(126,'Somali');
INSERT INTO languages VALUES(127,'Sotho');
INSERT INTO languages VALUES(128,'Southern Ndebele');
INSERT INTO languages VALUES(129,'Southern Sami');
INSERT INTO languages VALUES(130,'Spanish');
INSERT INTO languages VALUES(131,'Standard Moroccan Tamazight');
INSERT INTO languages VALUES(132,'Swahili');
INSERT INTO languages VALUES(133,'Swazi');
INSERT INTO languages VALUES(134,'Swedish');
INSERT INTO languages VALUES(135,'Swiss German');
INSERT INTO languages VALUES(136,'Tajik');
INSERT INTO languages VALUES(137,'Tamil');
INSERT INTO languages VALUES(138,'Tetum');
INSERT INTO languages VALUES(139,'Thai');
INSERT INTO languages VALUES(140,'Tigrinya');
INSERT INTO languages VALUES(141,'Tok Pisin');
INSERT INTO languages VALUES(142,'Tokelauan');
INSERT INTO languages VALUES(143,'Tonga (Zambia)');
INSERT INTO languages VALUES(144,'Tongan');
INSERT INTO languages VALUES(145,'Tsonga');
INSERT INTO languages VALUES(146,'Tswana');
INSERT INTO languages VALUES(147,'Turkish');
INSERT INTO languages VALUES(148,'Turkmen');
INSERT INTO languages VALUES(149,'Tuvaluan');
INSERT INTO languages VALUES(150,'Ukrainian');
INSERT INTO languages VALUES(151,'Upper Guinea Crioulo');
INSERT INTO languages VALUES(152,'Urdu');
INSERT INTO languages VALUES(153,'Uzbek');
INSERT INTO languages VALUES(154,'Venda');
INSERT INTO languages VALUES(155,'Vietnamese');
INSERT INTO languages VALUES(156,'Xhosa');
INSERT INTO languages VALUES(157,'Zimbabwean Sign Language');
INSERT INTO languages VALUES(158,'Zulu');
CREATE TABLE currencies (
	currency_id INTEGER NOT NULL, 
	code VARCHAR(3) NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	symbol VARCHAR(10) NOT NULL, 
	PRIMARY KEY (currency_id), 
	UNIQUE (code), 
	UNIQUE (name)
);
INSERT INTO currencies VALUES(1,'AED','United Arab Emirates dirham','د.إ');
INSERT INTO currencies VALUES(2,'AFN','Afghan afghani','؋');
INSERT INTO currencies VALUES(3,'ALL','Albanian lek','L');
INSERT INTO currencies VALUES(4,'AMD','Armenian dram','֏');
INSERT INTO currencies VALUES(5,'ANG','Netherlands Antillean guilder','ƒ');
INSERT INTO currencies VALUES(6,'AOA','Angolan kwanza','Kz');
INSERT INTO currencies VALUES(7,'ARS','Argentine peso','$');
INSERT INTO currencies VALUES(8,'AUD','Australian dollar','$');
INSERT INTO currencies VALUES(9,'AWG','Aruban florin','ƒ');
INSERT INTO currencies VALUES(10,'AZN','Azerbaijani manat','₼');
INSERT INTO currencies VALUES(11,'BAM','Bosnia and Herzegovina convertible mark','KM');
INSERT INTO currencies VALUES(12,'BBD','Barbadian dollar','$');
INSERT INTO currencies VALUES(13,'BDT','Bangladeshi taka','৳');
INSERT INTO currencies VALUES(14,'BGN','Bulgarian lev','лв');
INSERT INTO currencies VALUES(15,'BHD','Bahraini dinar','.د.ب');
INSERT INTO currencies VALUES(16,'BIF','Burundian franc','Fr');
INSERT INTO currencies VALUES(17,'BMD','Bermudian dollar','$');
INSERT INTO currencies VALUES(18,'BND','Brunei dollar','$');
INSERT INTO currencies VALUES(19,'BOB','Bolivian boliviano','Bs.');
INSERT INTO currencies VALUES(20,'BRL','Brazilian real','R$');
INSERT INTO currencies VALUES(21,'BSD','Bahamian dollar','$');
INSERT INTO currencies VALUES(22,'BTN','Bhutanese ngultrum','Nu.');
INSERT INTO currencies VALUES(23,'BWP','Botswana pula','P');
INSERT INTO currencies VALUES(24,'BYN','Belarusian ruble','Br');
INSERT INTO currencies VALUES(25,'BZD','Belize dollar','$');
INSERT INTO currencies VALUES(26,'CAD','Canadian dollar','$');
INSERT INTO currencies VALUES(27,'CDF','Congolese franc','FC');
INSERT INTO currencies VALUES(28,'CHF','Swiss franc','Fr');
INSERT INTO currencies VALUES(29,'CKD','Cook Islands dollar','$');
INSERT INTO currencies VALUES(30,'CLP','Chilean peso','$');
INSERT INTO currencies VALUES(31,'CNY','Chinese yuan','¥');
INSERT INTO currencies VALUES(32,'COP','Colombian peso','$');
INSERT INTO currencies VALUES(33,'CRC','Costa Rican colón','₡');
INSERT INTO currencies VALUES(34,'CUC','Cuban convertible peso','$');
INSERT INTO currencies VALUES(35,'CUP','Cuban peso','$');
INSERT INTO currencies VALUES(36,'CVE','Cape Verdean escudo','Esc');
INSERT INTO currencies VALUES(37,'CZK','Czech koruna','Kč');
INSERT INTO currencies VALUES(38,'DJF','Djiboutian franc','Fr');
INSERT INTO currencies VALUES(39,'DKK','Danish krone','kr');
INSERT INTO currencies VALUES(40,'DOP','Dominican peso','$');
INSERT INTO currencies VALUES(41,'DZD','Algerian dinar','د.ج');
INSERT INTO currencies VALUES(42,'EGP','Egyptian pound','£');
INSERT INTO currencies VALUES(43,'ERN','Eritrean nakfa','Nfk');
INSERT INTO currencies VALUES(44,'ETB','Ethiopian birr','Br');
INSERT INTO currencies VALUES(45,'EUR','Euro','€');
INSERT INTO currencies VALUES(46,'FJD','Fijian dollar','$');
INSERT INTO currencies VALUES(47,'FKP','Falkland Islands pound','£');
INSERT INTO currencies VALUES(48,'FOK','Faroese króna','kr');
INSERT INTO currencies VALUES(49,'GBP','Pound sterling','£');
INSERT INTO currencies VALUES(50,'GEL','lari','₾');
INSERT INTO currencies VALUES(51,'GGP','Guernsey pound','£');
INSERT INTO currencies VALUES(52,'GHS','Ghanaian cedi','₵');
INSERT INTO currencies VALUES(53,'GIP','Gibraltar pound','£');
INSERT INTO currencies VALUES(54,'GMD','dalasi','D');
INSERT INTO currencies VALUES(55,'GNF','Guinean franc','Fr');
INSERT INTO currencies VALUES(56,'GTQ','Guatemalan quetzal','Q');
INSERT INTO currencies VALUES(57,'GYD','Guyanese dollar','$');
INSERT INTO currencies VALUES(58,'HKD','Hong Kong dollar','$');
INSERT INTO currencies VALUES(59,'HNL','Honduran lempira','L');
INSERT INTO currencies VALUES(60,'HTG','Haitian gourde','G');
INSERT INTO currencies VALUES(61,'HUF','Hungarian forint','Ft');
INSERT INTO currencies VALUES(62,'IDR','Indonesian rupiah','Rp');
INSERT INTO currencies VALUES(63,'ILS','Israeli new shekel','₪');
INSERT INTO currencies VALUES(64,'IMP','Manx pound','£');
INSERT INTO currencies VALUES(65,'INR','Indian rupee','₹');
INSERT INTO currencies VALUES(66,'IQD','Iraqi dinar','ع.د');
INSERT INTO currencies VALUES(67,'IRR','Iranian rial','﷼');
INSERT INTO currencies VALUES(68,'ISK','Icelandic króna','kr');
INSERT INTO currencies VALUES(69,'JEP','Jersey pound','£');
INSERT INTO currencies VALUES(70,'JMD','Jamaican dollar','$');
INSERT INTO currencies VALUES(71,'JOD','Jordanian dinar','JD');
INSERT INTO currencies VALUES(72,'JPY','Japanese yen','¥');
INSERT INTO currencies VALUES(73,'KES','Kenyan shilling','Sh');
INSERT INTO currencies VALUES(74,'KGS','Kyrgyzstani som','с');
INSERT INTO currencies VALUES(75,'KHR','Cambodian riel','៛');
INSERT INTO currencies VALUES(76,'KID','Kiribati dollar','$');
INSERT INTO currencies VALUES(77,'KMF','Comorian franc','Fr');
INSERT INTO currencies VALUES(78,'KPW','North Korean won','₩');
INSERT INTO currencies VALUES(79,'KRW','South Korean won','₩');
INSERT INTO currencies VALUES(80,'KWD','Kuwaiti dinar','د.ك');
INSERT INTO currencies VALUES(81,'KYD','Cayman Islands dollar','$');
INSERT INTO currencies VALUES(82,'KZT','Kazakhstani tenge','₸');
INSERT INTO currencies VALUES(83,'LAK','Lao kip','₭');
INSERT INTO currencies VALUES(84,'LBP','Lebanese pound','ل.ل');
INSERT INTO currencies VALUES(85,'LKR','Sri Lankan rupee','Rs  රු');
INSERT INTO currencies VALUES(86,'LRD','Liberian dollar','$');
INSERT INTO currencies VALUES(87,'LSL','Lesotho loti','L');
INSERT INTO currencies VALUES(88,'LYD','Libyan dinar','ل.د');
INSERT INTO currencies VALUES(89,'MAD','Moroccan dirham','DH');
INSERT INTO currencies VALUES(90,'MDL','Moldovan leu','L');
INSERT INTO currencies VALUES(91,'MGA','Malagasy ariary','Ar');
INSERT INTO currencies VALUES(92,'MKD','denar','den');
INSERT INTO currencies VALUES(93,'MMK','Burmese kyat','Ks');
INSERT INTO currencies VALUES(94,'MNT','Mongolian tögrög','₮');
INSERT INTO currencies VALUES(95,'MOP','Macanese pataca','P');
INSERT INTO currencies VALUES(96,'MRU','Mauritanian ouguiya','UM');
INSERT INTO currencies VALUES(97,'MUR','Mauritian rupee','₨');
INSERT INTO currencies VALUES(98,'MVR','Maldivian rufiyaa','.ރ');
INSERT INTO currencies VALUES(99,'MWK','Malawian kwacha','MK');
INSERT INTO currencies VALUES(100,'MXN','Mexican peso','$');
INSERT INTO currencies VALUES(101,'MYR','Malaysian ringgit','RM');
INSERT INTO currencies VALUES(102,'MZN','Mozambican metical','MT');
INSERT INTO currencies VALUES(103,'NAD','Namibian dollar','$');
INSERT INTO currencies VALUES(104,'NGN','Nigerian naira','₦');
INSERT INTO currencies VALUES(105,'NIO','Nicaraguan córdoba','C$');
INSERT INTO currencies VALUES(106,'NOK','Norwegian krone','kr');
INSERT INTO currencies VALUES(107,'NPR','Nepalese rupee','₨');
INSERT INTO currencies VALUES(108,'NZD','New Zealand dollar','$');
INSERT INTO currencies VALUES(109,'OMR','Omani rial','ر.ع.');
INSERT INTO currencies VALUES(110,'PAB','Panamanian balboa','B/.');
INSERT INTO currencies VALUES(111,'PEN','Peruvian sol','S/ ');
INSERT INTO currencies VALUES(112,'PGK','Papua New Guinean kina','K');
INSERT INTO currencies VALUES(113,'PHP','Philippine peso','₱');
INSERT INTO currencies VALUES(114,'PKR','Pakistani rupee','₨');
INSERT INTO currencies VALUES(115,'PLN','Polish złoty','zł');
INSERT INTO currencies VALUES(116,'PYG','Paraguayan guaraní','₲');
INSERT INTO currencies VALUES(117,'QAR','Qatari riyal','ر.ق');
INSERT INTO currencies VALUES(118,'RON','Romanian leu','lei');
INSERT INTO currencies VALUES(119,'RSD','Serbian dinar','дин.');
INSERT INTO currencies VALUES(120,'RUB','Russian ruble','₽');
INSERT INTO currencies VALUES(121,'RWF','Rwandan franc','Fr');
INSERT INTO currencies VALUES(122,'SAR','Saudi riyal','ر.س');
INSERT INTO currencies VALUES(123,'SBD','Solomon Islands dollar','$');
INSERT INTO currencies VALUES(124,'SCR','Seychellois rupee','₨');
INSERT INTO currencies VALUES(125,'SDG','Sudanese pound','ج.س');
INSERT INTO currencies VALUES(126,'SEK','Swedish krona','kr');
INSERT INTO currencies VALUES(127,'SGD','Singapore dollar','$');
INSERT INTO currencies VALUES(128,'SHP','Saint Helena pound','£');
INSERT INTO currencies VALUES(129,'SLE','Leone','Le');
INSERT INTO currencies VALUES(130,'SLSH','Somaliland shilling','Sl.Sh');
INSERT INTO currencies VALUES(131,'SOS','Somali shilling','Sh');
INSERT INTO currencies VALUES(132,'SRD','Surinamese dollar','$');
INSERT INTO currencies VALUES(133,'SSP','South Sudanese pound','£');
INSERT INTO currencies VALUES(134,'STN','São Tomé and Príncipe dobra','Db');
INSERT INTO currencies VALUES(135,'SYP','Syrian pound','£');
INSERT INTO currencies VALUES(136,'SZL','Swazi lilangeni','L');
INSERT INTO currencies VALUES(137,'THB','Thai baht','฿');
INSERT INTO currencies VALUES(138,'TJS','Tajikistani somoni','ЅМ');
INSERT INTO currencies VALUES(139,'TMT','Turkmenistan manat','m');
INSERT INTO currencies VALUES(140,'TND','Tunisian dinar','د.ت');
INSERT INTO currencies VALUES(141,'TOP','Tongan paʻanga','T$');
INSERT INTO currencies VALUES(142,'TRY','Turkish lira','₺');
INSERT INTO currencies VALUES(143,'TTD','Trinidad and Tobago dollar','$');
INSERT INTO currencies VALUES(144,'TVD','Tuvaluan dollar','$');
INSERT INTO currencies VALUES(145,'TWD','New Taiwan dollar','$');
INSERT INTO currencies VALUES(146,'TZS','Tanzanian shilling','Sh');
INSERT INTO currencies VALUES(147,'UAH','Ukrainian hryvnia','₴');
INSERT INTO currencies VALUES(148,'UGX','Ugandan shilling','Sh');
INSERT INTO currencies VALUES(149,'USD','United States dollar','$');
INSERT INTO currencies VALUES(150,'UYU','Uruguayan peso','$');
INSERT INTO currencies VALUES(151,'UZS','Uzbekistani soʻm','so''m');
INSERT INTO currencies VALUES(152,'VES','Venezuelan bolívar soberano','Bs.S.');
INSERT INTO currencies VALUES(153,'VND','Vietnamese đồng','₫');
INSERT INTO currencies VALUES(154,'VUV','Vanuatu vatu','Vt');
INSERT INTO currencies VALUES(155,'WST','Samoan tālā','T');
INSERT INTO currencies VALUES(156,'XAF','Central African CFA franc','Fr');
INSERT INTO currencies VALUES(157,'XCD','Eastern Caribbean dollar','$');
INSERT INTO currencies VALUES(158,'XOF','West African CFA franc','Fr');
INSERT INTO currencies VALUES(159,'XPF','CFP franc','₣');
INSERT INTO currencies VALUES(160,'YER','Yemeni rial','﷼');
INSERT INTO currencies VALUES(161,'ZAR','South African rand','R');
INSERT INTO currencies VALUES(162,'ZMW','Zambian kwacha','ZK');
INSERT INTO currencies VALUES(163,'ZWL','Zimbabwean dollar','$');
CREATE TABLE subregions (
	subregion_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	region_id INTEGER NOT NULL, 
	PRIMARY KEY (subregion_id), 
	UNIQUE (name), 
	FOREIGN KEY(region_id) REFERENCES regions (region_id) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO subregions VALUES(1,'Eastern Africa',1);
INSERT INTO subregions VALUES(2,'Middle Africa',1);
INSERT INTO subregions VALUES(3,'Northern Africa',1);
INSERT INTO subregions VALUES(4,'Southern Africa',1);
INSERT INTO subregions VALUES(5,'Western Africa',1);
INSERT INTO subregions VALUES(6,'Caribbean',2);
INSERT INTO subregions VALUES(7,'Central America',2);
INSERT INTO subregions VALUES(8,'North America',2);
INSERT INTO subregions VALUES(9,'South America',2);
INSERT INTO subregions VALUES(10,'Central Asia',4);
INSERT INTO subregions VALUES(11,'Eastern Asia',4);
INSERT INTO subregions VALUES(12,'South-Eastern Asia',4);
INSERT INTO subregions VALUES(13,'Southern Asia',4);
INSERT INTO subregions VALUES(14,'Western Asia',4);
INSERT INTO subregions VALUES(15,'Central Europe',5);
INSERT INTO subregions VALUES(16,'Eastern Europe',5);
INSERT INTO subregions VALUES(17,'Northern Europe',5);
INSERT INTO subregions VALUES(18,'Southeast Europe',5);
INSERT INTO subregions VALUES(19,'Southern Europe',5);
INSERT INTO subregions VALUES(20,'Western Europe',5);
INSERT INTO subregions VALUES(21,'Australia and New Zealand',6);
INSERT INTO subregions VALUES(22,'Melanesia',6);
INSERT INTO subregions VALUES(23,'Micronesia',6);
INSERT INTO subregions VALUES(24,'Polynesia',6);
CREATE TABLE countries (
	country_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	official_name VARCHAR(255) NOT NULL, 
	code VARCHAR(2) NOT NULL, 
	area REAL NOT NULL, 
	tld VARCHAR(10) NOT NULL, 
	flag VARCHAR(10) NOT NULL, 
	population INTEGER NOT NULL, 
	currency INTEGER NOT NULL, 
	language_id INTEGER NOT NULL, 
	googlemaps TEXT NOT NULL, 
	openstreetmaps TEXT NOT NULL, 
	subregion_id INTEGER DEFAULT null, 
	PRIMARY KEY (country_id), 
	UNIQUE (name), 
	UNIQUE (official_name), 
	FOREIGN KEY(currency) REFERENCES currencies (currency_id) ON DELETE RESTRICT ON UPDATE CASCADE, 
	FOREIGN KEY(language_id) REFERENCES languages (language_id) ON DELETE RESTRICT ON UPDATE CASCADE, 
	FOREIGN KEY(subregion_id) REFERENCES subregions (subregion_id) ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO countries VALUES(1,'Abkhazia','Republic of Abkhazia','',8665.0,'','',244000,120,1,'','',14);
INSERT INTO countries VALUES(2,'Afghanistan','Islamic Republic of Afghanistan','AF',652230.0,'.af','🇦🇫',35000000,2,30,'https://goo.gl/maps/BXBGw7yUUFknCfva9','https://www.openstreetmap.org/relation/303427',13);
INSERT INTO countries VALUES(3,'Albania','Republic of Albania','AL',28748.0,'.al','🇦🇱',2402113,3,3,'https://goo.gl/maps/BzN9cTuj68ZA8SyZ8','https://www.openstreetmap.org/relation/53292',18);
INSERT INTO countries VALUES(4,'Algeria','People''s Democratic Republic of Algeria','DZ',2381741.0,'.dz','🇩🇿',47400000,41,5,'https://goo.gl/maps/RsAyAfyaiNVb8DpW8','https://www.openstreetmap.org/relation/192756',3);
INSERT INTO countries VALUES(5,'American Samoa','American Samoa','AS',199.0,'.as','🇦🇸',43268,149,34,'https://goo.gl/maps/Re9ePMjwP1sFCBFA6','https://www.openstreetmap.org/relation/2177187',24);
INSERT INTO countries VALUES(6,'Andorra','Principality of Andorra','AD',468.0,'.ad','🇦🇩',89368,45,21,'https://goo.gl/maps/JqAnacWE2qEznKgw7','https://www.openstreetmap.org/relation/9407',19);
INSERT INTO countries VALUES(7,'Angola','Republic of Angola','AO',1246700.0,'.ao','🇦🇴',36604681,6,112,'https://goo.gl/maps/q42Qbf1BmQL3fuZg9','https://www.openstreetmap.org/relation/195267',2);
INSERT INTO countries VALUES(8,'Anguilla','Anguilla','AI',91.0,'.ai','🇦🇮',16010,157,34,'https://goo.gl/maps/3KgLnEyN7amdno2p9','https://www.openstreetmap.org/relation/2177161',6);
INSERT INTO countries VALUES(9,'Antarctica','Antarctica','AQ',14000000.0,'.aq','🇦🇶',1300,149,34,'https://goo.gl/maps/kyBuJriu4itiXank7','https://www.openstreetmap.org/node/36966060',NULL);
INSERT INTO countries VALUES(10,'Antigua and Barbuda','Antigua and Barbuda','AG',442.0,'.ag','🇦🇬',106365,157,34,'https://goo.gl/maps/fnye4wGJ1RzC9jpX9','https://www.openstreetmap.org/relation/536900',6);
INSERT INTO countries VALUES(11,'Argentina','Argentine Republic','AR',2780400.0,'.ar','🇦🇷',46735004,7,48,'https://goo.gl/maps/Z9DXNxhf2o93kvyc6','https://www.openstreetmap.org/relation/286393',9);
INSERT INTO countries VALUES(12,'Armenia','Republic of Armenia','AM',29743.0,'.am','🇦🇲',3081100,4,8,'https://goo.gl/maps/azWUtK9bUQYEyccbA','https://www.openstreetmap.org/relation/364066',14);
INSERT INTO countries VALUES(13,'Aruba','Aruba','AW',180.0,'.aw','🇦🇼',108880,9,32,'https://goo.gl/maps/8hopbQqifHAgyZyg8','https://www.openstreetmap.org/relation/1231749',6);
INSERT INTO countries VALUES(14,'Australia','Commonwealth of Australia','AU',7692024.0,'.au','🇦🇺',27724744,8,34,'https://goo.gl/maps/DcjaDa7UbhnZTndH6','https://www.openstreetmap.org/relation/80500',21);
INSERT INTO countries VALUES(15,'Austria','Republic of Austria','AT',83871.0,'.at','🇦🇹',9219113,45,44,'https://goo.gl/maps/pCWpWQhznHyRzQcu9','https://www.openstreetmap.org/relation/16239',15);
INSERT INTO countries VALUES(16,'Azerbaijan','Republic of Azerbaijan','AZ',86600.0,'.az','🇦🇿',10353296,10,10,'https://goo.gl/maps/az3Zz7ar2aoB9AUc6','https://www.openstreetmap.org/relation/364110',14);
INSERT INTO countries VALUES(17,'Bahamas','Commonwealth of the Bahamas','BS',13943.0,'.bs','🇧🇸',398165,21,34,'https://goo.gl/maps/1YzRs1BZrG8p8pmVA','https://www.openstreetmap.org/relation/547469',6);
INSERT INTO countries VALUES(18,'Bahrain','Kingdom of Bahrain','BH',765.0,'.bh','🇧🇭',1501635,15,5,'https://goo.gl/maps/5Zue99Zc6vFBHxzJ7','https://www.openstreetmap.org/relation/378734',14);
INSERT INTO countries VALUES(19,'Bangladesh','People''s Republic of Bangladesh','BD',147570.0,'.bd','🇧🇩',175423000,13,15,'https://goo.gl/maps/op6gmLbHcvv6rLhH6','https://www.openstreetmap.org/relation/184640',13);
INSERT INTO countries VALUES(20,'Barbados','Barbados','BB',430.0,'.bb','🇧🇧',281998,12,34,'https://goo.gl/maps/2m36v8STvbGAWd9c7','https://www.openstreetmap.org/relation/547511',6);
INSERT INTO countries VALUES(21,'Belarus','Republic of Belarus','BY',207600.0,'.by','🇧🇾',9109280,24,13,'https://goo.gl/maps/PJUDU3EBPSszCQcu6','https://www.openstreetmap.org/relation/59065',16);
INSERT INTO countries VALUES(22,'Belgium','Kingdom of Belgium','BE',30528.0,'.be','🇧🇪',11867634,45,44,'https://goo.gl/maps/UQQzat85TCtPRXAL8','https://www.openstreetmap.org/relation/52411',20);
INSERT INTO countries VALUES(23,'Belize','Belize','BZ',22966.0,'.bz','🇧🇿',397483,25,14,'https://goo.gl/maps/jdCccpdLodm1uTmo9','https://www.openstreetmap.org/relation/287827',7);
INSERT INTO countries VALUES(24,'Benin','Republic of Benin','BJ',112622.0,'.bj','🇧🇯',13754688,158,41,'https://goo.gl/maps/uMw1BsHEXQYgVFFu6','https://www.openstreetmap.org/relation/192784',5);
INSERT INTO countries VALUES(25,'Bermuda','Bermuda','BM',54.0,'.bm','🇧🇲',63913,17,34,'https://goo.gl/maps/NLsRGNjTzDghTtAJA','https://www.openstreetmap.org/relation/1993208',8);
INSERT INTO countries VALUES(26,'Bhutan','Kingdom of Bhutan','BT',38394.0,'.bt','🇧🇹',727145,22,33,'https://goo.gl/maps/VEfXXBftTFLUpNgp8','https://www.openstreetmap.org/relation/184629',13);
INSERT INTO countries VALUES(27,'Bolivia','Plurinational State of Bolivia','BO',1098581.0,'.bo','🇧🇴',11365333,19,9,'https://goo.gl/maps/9DfnyfbxNM2g5U9b9','https://www.openstreetmap.org/relation/252645',9);
INSERT INTO countries VALUES(28,'Bosnia and Herzegovina','Bosnia and Herzegovina','BA',51209.0,'.ba','🇧🇦',3412000,11,17,'https://www.google.com/maps/place/Bosnia+and+Herzegovina','https://www.openstreetmap.org/relation/2528142',18);
INSERT INTO countries VALUES(29,'Botswana','Republic of Botswana','BW',582000.0,'.bw','🇧🇼',2359609,23,34,'https://goo.gl/maps/E364KeLy6N4JwxwQ8','https://www.openstreetmap.org/relation/1889339',4);
INSERT INTO countries VALUES(30,'Bouvet Island','Bouvet Island','BV',49.0,'.bv','🇧🇻',0,149,103,'https://goo.gl/maps/7WRQAEKZb4uK36yi9','https://www.openstreetmap.org/way/174996681',NULL);
INSERT INTO countries VALUES(31,'Brazil','Federative Republic of Brazil','BR',8515767.0,'.br','🇧🇷',213421037,20,112,'https://goo.gl/maps/waCKk21HeeqFzkNC9','https://www.openstreetmap.org/relation/59470',9);
INSERT INTO countries VALUES(32,'British Indian Ocean Territory','British Indian Ocean Territory','IO',60.0,'.io','🇮🇴',2000,149,34,'https://goo.gl/maps/bheNucgekVEYozoi6','https://www.openstreetmap.org/relation/1993867',1);
INSERT INTO countries VALUES(33,'British Virgin Islands','Virgin Islands','VG',151.0,'.vg','🇻🇬',38322,149,34,'https://goo.gl/maps/49C9cSesNVAR9DQk8','https://www.openstreetmap.org/relation/285454',6);
INSERT INTO countries VALUES(34,'Brunei','Nation of Brunei, the Abode of Peace','BN',5765.0,'.bn','🇧🇳',458600,18,83,'https://goo.gl/maps/4jb4CqBXhr8vNh579','https://www.openstreetmap.org/relation/2103120',12);
INSERT INTO countries VALUES(35,'Bulgaria','Republic of Bulgaria','BG',110879.0,'.bg','🇧🇬',6423207,14,18,'https://goo.gl/maps/F5uAhDGWzc3BrHfm9','https://www.openstreetmap.org/relation/186382',18);
INSERT INTO countries VALUES(36,'Burkina Faso','Burkina Faso','BF',272967.0,'.bf','🇧🇫',22489126,158,41,'https://goo.gl/maps/rKRmpcMbFher2ozb7','https://www.openstreetmap.org/relation/192783',5);
INSERT INTO countries VALUES(37,'Burundi','Republic of Burundi','BI',27834.0,'.bi','🇧🇮',14151540,16,41,'https://goo.gl/maps/RXPWoRrB9tfrJpUG7','https://www.openstreetmap.org/relation/195269',1);
INSERT INTO countries VALUES(38,'Cabo Verde','Republic of Cabo Verde','CV',4033.0,'.cv','🇨🇻',491233,36,112,'https://goo.gl/maps/Kc9vy5ChjuiAgMfXA','https://www.openstreetmap.org/relation/535774',5);
INSERT INTO countries VALUES(39,'Cambodia','Kingdom of Cambodia','KH',181035.0,'.kh','🇰🇭',17638801,75,65,'https://goo.gl/maps/nztQtFSrUXZymJaW8','https://www.openstreetmap.org/relation/49898',12);
INSERT INTO countries VALUES(40,'Cameroon','Republic of Cameroon','CM',475442.0,'.cm','🇨🇲',30987821,156,34,'https://goo.gl/maps/JqiipHgFboG3rBJh9','https://www.openstreetmap.org/relation/192830',2);
INSERT INTO countries VALUES(41,'Canada','Canada','CA',9984670.0,'.ca','🇨🇦',41575585,26,34,'https://goo.gl/maps/jmEVLugreeqiZXxbA','https://www.openstreetmap.org/relation/1428125',8);
INSERT INTO countries VALUES(42,'Caribbean Netherlands','Bonaire, Sint Eustatius and Saba','BQ',328.0,'.bq','🇧🇶',31980,149,34,'https://goo.gl/maps/4XVes1P6uEDTz77WA','https://www.openstreetmap.org/relation/1216720',6);
INSERT INTO countries VALUES(43,'Cayman Islands','Cayman Islands','KY',264.0,'.ky','🇰🇾',90577,81,34,'https://goo.gl/maps/P3ZVXX3LH63t91hL8','https://www.openstreetmap.org/relation/7269765',6);
INSERT INTO countries VALUES(44,'Central African Republic','Central African Republic','CF',622984.0,'.cf','🇨🇫',5513282,156,41,'https://goo.gl/maps/51V8dsi2rGYC9n3c9','https://www.openstreetmap.org/relation/192790',2);
INSERT INTO countries VALUES(45,'Chad','Republic of Chad','TD',1284000.0,'.td','🇹🇩',19093595,156,5,'https://goo.gl/maps/ziUdAZ8skuNfx5Hx7','https://www.openstreetmap.org/relation/2361304',2);
INSERT INTO countries VALUES(46,'Chile','Republic of Chile','CL',756102.0,'.cl','🇨🇱',19629588,30,130,'https://goo.gl/maps/XboxyNHh2fAjCPNn9','https://www.openstreetmap.org/relation/167454',9);
INSERT INTO countries VALUES(47,'China','People''s Republic of China','CN',9706961.0,'.cn','🇨🇳',1404890000,31,25,'https://goo.gl/maps/p9qC6vgiFRRXzvGi7','https://www.openstreetmap.org/relation/270056',11);
INSERT INTO countries VALUES(48,'Christmas Island','Territory of Christmas Island','CX',135.0,'.cx','🇨🇽',1692,8,34,'https://goo.gl/maps/ZC17hHsQZpShN5wk9','https://www.openstreetmap.org/relation/6365444',21);
INSERT INTO countries VALUES(49,'Cocos (Keeling) Islands','Territory of the Cocos (Keeling) Islands','CC',14.0,'.cc','🇨🇨',593,8,34,'https://goo.gl/maps/3eCdKVpVfMcZyKcK6','https://www.openstreetmap.org/relation/82636',21);
INSERT INTO countries VALUES(50,'Colombia','Republic of Colombia','CO',1141748.0,'.co','🇨🇴',52695952,32,130,'https://goo.gl/maps/zix9qNFX69E9yZ2M6','https://www.openstreetmap.org/relation/120027',9);
INSERT INTO countries VALUES(51,'Comoros','Union of the Comoros','KM',1862.0,'.km','🇰🇲',944388,77,5,'https://goo.gl/maps/eas4GP28C1GyStnu6','https://www.openstreetmap.org/relation/535790',1);
INSERT INTO countries VALUES(52,'Congo','Republic of the Congo','CG',342000.0,'.cg','🇨🇬',6228784,156,41,'https://goo.gl/maps/Phf5dDDKdfCtuBTb6','https://www.openstreetmap.org/relation/192794',2);
INSERT INTO countries VALUES(53,'Cook Islands','Cook Islands','CK',236.0,'.ck','🇨🇰',15040,29,34,'https://goo.gl/maps/nrGZrvWRGB4WHgDC9','https://www.openstreetmap.org/relation/2184233',24);
INSERT INTO countries VALUES(54,'Costa Rica','Republic of Costa Rica','CR',51100.0,'.cr','🇨🇷',5160700,33,130,'https://goo.gl/maps/RFiwytjvNrpfKN7k6','https://www.openstreetmap.org/relation/287667',7);
INSERT INTO countries VALUES(55,'Croatia','Republic of Croatia','HR',56594.0,'.hr','🇭🇷',3866233,45,27,'https://goo.gl/maps/qSG6xTKUmrYpwmGQ6','https://www.openstreetmap.org/relation/214885',18);
INSERT INTO countries VALUES(56,'Cuba','Republic of Cuba','CU',109884.0,'.cu','🇨🇺',9748007,34,130,'https://goo.gl/maps/1dDw1QfZspfMUTm99','https://www.openstreetmap.org/relation/307833',6);
INSERT INTO countries VALUES(57,'Curaçao','Country of Curaçao','CW',444.0,'.cw','🇨🇼',155826,5,34,'https://goo.gl/maps/9D3hTeA3qKaRT7S16','https://www.openstreetmap.org/relation/1216719',6);
INSERT INTO countries VALUES(58,'Cyprus','Republic of Cyprus','CY',9251.0,'.cy','🇨🇾',923272,45,46,'https://goo.gl/maps/77hPBRdLid8yD5Bm7','https://www.openstreetmap.org/relation/307787',19);
INSERT INTO countries VALUES(59,'Czechia','Czech Republic','CZ',78865.0,'.cz','🇨🇿',10915839,37,28,'https://goo.gl/maps/47dmgeXMZyhDHyQW8','https://www.openstreetmap.org/relation/51684',15);
INSERT INTO countries VALUES(60,'DRC','Democratic Republic of the Congo','CD',2344858.0,'.cd','🇨🇩',124388160,27,41,'https://goo.gl/maps/KfhNVn6VqdZXWu8n9','https://www.openstreetmap.org/relation/192795',2);
INSERT INTO countries VALUES(61,'Denmark','Kingdom of Denmark','DK',43094.0,'.dk','🇩🇰',6001008,39,29,'https://goo.gl/maps/UddGPN7hAyrtpFiT6','https://www.openstreetmap.org/relation/50046',17);
INSERT INTO countries VALUES(62,'Djibouti','Republic of Djibouti','DJ',23200.0,'.dj','🇩🇯',1066809,38,5,'https://goo.gl/maps/V1HWfzN3bS1kwf4C6','https://www.openstreetmap.org/relation/192801',1);
INSERT INTO countries VALUES(63,'Dominica','Commonwealth of Dominica','DM',751.0,'.dm','🇩🇲',71293,157,34,'https://goo.gl/maps/HSKdHYpFC8oHHuyV7','https://www.openstreetmap.org/relation/307823',6);
INSERT INTO countries VALUES(64,'Dominican Republic','Dominican Republic','DO',48671.0,'.do','🇩🇴',11532151,40,130,'https://goo.gl/maps/soxooTHxEeiAbn3UA','https://www.openstreetmap.org/relation/307828',6);
INSERT INTO countries VALUES(65,'Ecuador','Republic of Ecuador','EC',276841.0,'.ec','🇪🇨',17483326,149,130,'https://goo.gl/maps/TbX8hUW4gcbRPZiK7','https://www.openstreetmap.org/relation/108089',9);
INSERT INTO countries VALUES(66,'Egypt','Arab Republic of Egypt','EG',1002450.0,'.eg','🇪🇬',107868296,42,5,'https://goo.gl/maps/uoDRhXbsqjG6L7VG7','https://www.openstreetmap.org/relation/1473947',3);
INSERT INTO countries VALUES(67,'El Salvador','Republic of El Salvador','SV',21041.0,'.sv','🇸🇻',6029976,149,130,'https://goo.gl/maps/cZnCEi5sEMQtKKcB7','https://www.openstreetmap.org/relation/1520612',7);
INSERT INTO countries VALUES(68,'Equatorial Guinea','Republic of Equatorial Guinea','GQ',28051.0,'.gq','🇬🇶',1795834,156,41,'https://goo.gl/maps/ucWfFd8aW1FbGMva9','https://www.openstreetmap.org/relation/192791',2);
INSERT INTO countries VALUES(69,'Eritrea','State of Eritrea','ER',117600.0,'.er','🇪🇷',3500000,43,5,'https://goo.gl/maps/HRyqUpnPwwG6jY5j6','https://www.openstreetmap.org/relation/296961',1);
INSERT INTO countries VALUES(70,'Estonia','Republic of Estonia','EE',45227.0,'.ee','🇪🇪',1362954,45,35,'https://goo.gl/maps/6SsynwGUodL1sDvq8','https://www.openstreetmap.org/relation/79510',17);
INSERT INTO countries VALUES(71,'Eswatini','Kingdom of Eswatini','SZ',17364.0,'.sz','🇸🇿',1236126,136,34,'https://goo.gl/maps/cUY79eqQihFSE8hV6','https://www.openstreetmap.org/relation/88210',4);
INSERT INTO countries VALUES(72,'Ethiopia','Federal Democratic Republic of Ethiopia','ET',1104300.0,'.et','🇪🇹',135500000,44,4,'https://goo.gl/maps/2Q4hQWCbhuZLj3fG6','https://www.openstreetmap.org/relation/192800',1);
INSERT INTO countries VALUES(73,'Falkland Islands','Falkland Islands','FK',12173.0,'.fk','🇫🇰',3662,47,34,'https://goo.gl/maps/TZH1x7AGanQKifNk7','https://www.openstreetmap.org/relation/2185374',9);
INSERT INTO countries VALUES(74,'Faroe Islands','Faroe Islands','FO',1393.0,'.fo','🇫🇴',56210,39,29,'https://goo.gl/maps/6sTru4SmHdEVcNkM6','https://www.openstreetmap.org/relation/52939',17);
INSERT INTO countries VALUES(75,'Fiji','Republic of Fiji','FJ',18272.0,'.fj','🇫🇯',926276,46,34,'https://goo.gl/maps/r9fhDqoLZdg1zmE99','https://www.openstreetmap.org/relation/571747',22);
INSERT INTO countries VALUES(76,'Finland','Republic of Finland','FI',338424.0,'.fi','🇫🇮',5652881,45,40,'https://goo.gl/maps/HjgWDCNKRAYHrkMn8','https://www.openstreetmap.org/relation/54224',17);
INSERT INTO countries VALUES(77,'France','French Republic','FR',551695.0,'.fr','🇫🇷',69081996,45,41,'https://goo.gl/maps/g7QxxSFsWyTPKuzd7','https://www.openstreetmap.org/relation/1403916',20);
INSERT INTO countries VALUES(78,'French Guiana','Guiana','GF',83534.0,'.gf','🇬🇫',254541,45,41,'https://goo.gl/maps/NJawFwMzG7YtCrVP7','https://www.openstreetmap.org/relation/2502058',9);
INSERT INTO countries VALUES(79,'French Polynesia','French Polynesia','PF',4167.0,'.pf','🇵🇫',278786,159,41,'https://goo.gl/maps/xgg6BQTRyeQg4e1m6','https://www.openstreetmap.org/relation/3412620',24);
INSERT INTO countries VALUES(80,'French Southern and Antarctic Lands','Territory of the French Southern and Antarctic Lands','TF',7747.0,'.tf','🇹🇫',400,45,41,'https://goo.gl/maps/6ua6CX1m4w1xF2Em7','https://www.openstreetmap.org/relation/2186658',NULL);
INSERT INTO countries VALUES(81,'Gabon','Gabonese Republic','GA',267668.0,'.ga','🇬🇦',2397368,156,41,'https://goo.gl/maps/vyRSkqw1H1fnq4ry6','https://www.openstreetmap.org/relation/192793',2);
INSERT INTO countries VALUES(82,'Gambia','Republic of the Gambia','GM',10689.0,'.gm','🇬🇲',2422712,54,34,'https://goo.gl/maps/bbGBCxxtfD2A9Z4m6','https://www.openstreetmap.org/relation/192774',5);
INSERT INTO countries VALUES(83,'Georgia','Georgia','GE',69700.0,'.ge','🇬🇪',3657000,50,43,'https://goo.gl/maps/bvCaGBePR1ZEDK5cA','https://www.openstreetmap.org/relation/28699',14);
INSERT INTO countries VALUES(84,'Germany','Federal Republic of Germany','DE',357114.0,'.de','🇩🇪',83497147,45,44,'https://goo.gl/maps/mD9FBMq1nvXUBrkv6','https://www.openstreetmap.org/relation/51477',20);
INSERT INTO countries VALUES(85,'Ghana','Republic of Ghana','GH',238533.0,'.gh','🇬🇭',35039451,52,34,'https://goo.gl/maps/Avy5RSmdsXFBaiXq8','https://www.openstreetmap.org/relation/192781',5);
INSERT INTO countries VALUES(86,'Gibraltar','Gibraltar','GI',6.0,'.gi','🇬🇮',37936,53,34,'https://goo.gl/maps/CEoHAs1t6byCBhHFA','https://www.openstreetmap.org/relation/1278736',19);
INSERT INTO countries VALUES(87,'Greece','Hellenic Republic','GR',131990.0,'.gr','🇬🇷',10718565,45,46,'https://goo.gl/maps/LHGcAvuRyD2iKECC6','https://www.openstreetmap.org/relation/192307',19);
INSERT INTO countries VALUES(88,'Greenland','Greenland','GL',2166086.0,'.gl','🇬🇱',56831,39,47,'https://goo.gl/maps/j3289UPEQXt1ceSy8','https://www.openstreetmap.org/relation/2184073',8);
INSERT INTO countries VALUES(89,'Grenada','Grenada','GD',344.0,'.gd','🇬🇩',114621,157,34,'https://goo.gl/maps/rqWyfUAt4xhvk1Zy9','https://www.openstreetmap.org/relation/550727',6);
INSERT INTO countries VALUES(90,'Guadeloupe','Guadeloupe','GP',1628.0,'.gp','🇬🇵',400132,45,41,'https://goo.gl/maps/Dy9R2EufJtoWm8UN9','https://www.openstreetmap.org/relation/7109289',6);
INSERT INTO countries VALUES(91,'Guam','Guam','GU',549.0,'.gu','🇬🇺',165180,149,23,'https://goo.gl/maps/Xfnq2i279b18cH3C9','https://www.openstreetmap.org/relation/306001',23);
INSERT INTO countries VALUES(92,'Guatemala','Republic of Guatemala','GT',108889.0,'.gt','🇬🇹',18636532,56,130,'https://goo.gl/maps/JoRAbem4Hxb9FYbVA','https://www.openstreetmap.org/relation/1521463',7);
INSERT INTO countries VALUES(93,'Guernsey','Bailiwick of Guernsey','GG',78.0,'.gg','🇬🇬',63950,49,34,'https://goo.gl/maps/6kXnQU5QvEZMD9VB7','https://www.openstreetmap.org/relation/270009',17);
INSERT INTO countries VALUES(94,'Guinea','Republic of Guinea','GN',245857.0,'.gn','🇬🇳',13986179,55,41,'https://goo.gl/maps/8J5oM5sA4Ayr1ZYGA','https://www.openstreetmap.org/relation/192778',5);
INSERT INTO countries VALUES(95,'Guinea-Bissau','Republic of Guinea-Bissau','GW',36125.0,'.gw','🇬🇼',2080000,158,112,'https://goo.gl/maps/5Wyaz17miUc1zLc67','https://www.openstreetmap.org/relation/192776',5);
INSERT INTO countries VALUES(96,'Guyana','Co-operative Republic of Guyana','GY',214969.0,'.gy','🇬🇾',950986,57,34,'https://goo.gl/maps/DFsme2xEeugUAsCx5','https://www.openstreetmap.org/relation/287083',9);
INSERT INTO countries VALUES(97,'Haiti','Republic of Haiti','HT',27750.0,'.ht','🇭🇹',11470261,60,41,'https://goo.gl/maps/9o13xtjuUdqFnHbn9','https://www.openstreetmap.org/relation/307829',6);
INSERT INTO countries VALUES(98,'Heard Island and McDonald Islands','Heard Island and McDonald Islands','HM',412.0,'.hm','🇭🇲',0,149,34,'https://goo.gl/maps/k5FBAiVaVyozuYeA7','https://www.openstreetmap.org/relation/2177227',NULL);
INSERT INTO countries VALUES(99,'Honduras','Republic of Honduras','HN',112492.0,'.hn','🇭🇳',9571352,59,130,'https://goo.gl/maps/BbeJK8Sk2VkMHbdF8','https://www.openstreetmap.org/relation/287670',7);
INSERT INTO countries VALUES(100,'Hong Kong','Hong Kong Special Administrative Region of the People''s Republic of China','HK',1104.0,'.hk','🇭🇰',7498100,58,34,'https://goo.gl/maps/1sEnNmT47ffrC8MU8','https://www.openstreetmap.org/relation/913110',11);
INSERT INTO countries VALUES(101,'Hungary','Hungary','HU',93028.0,'.hu','🇭🇺',9489000,61,56,'https://goo.gl/maps/9gfPupm5bffixiFJ6','https://www.openstreetmap.org/relation/21335',15);
INSERT INTO countries VALUES(102,'Iceland','Iceland','IS',103000.0,'.is','🇮🇸',394324,68,57,'https://goo.gl/maps/WxFWSQuc3oamNxoE6','https://www.openstreetmap.org/relation/299133',17);
INSERT INTO countries VALUES(103,'India','Republic of India','IN',3287590.0,'.in','🇮🇳',1380004385,65,34,'https://goo.gl/maps/WSk3fLwG4vtPQetp7','https://www.openstreetmap.org/relation/304716',13);
INSERT INTO countries VALUES(104,'Indonesia','Republic of Indonesia','ID',1904569.0,'.id','🇮🇩',288315089,62,58,'https://goo.gl/maps/9gfPupm5bffixiFJ6','https://www.openstreetmap.org/relation/21335',12);
INSERT INTO countries VALUES(105,'Iran','Islamic Republic of Iran','IR',1648195.0,'.ir','🇮🇷',92417681,67,110,'https://goo.gl/maps/dMgEGuacBPGYQnjY7','https://www.openstreetmap.org/relation/304938',13);
INSERT INTO countries VALUES(106,'Iraq','Republic of Iraq','IQ',438317.0,'.iq','🇮🇶',46118793,66,5,'https://goo.gl/maps/iL8Bmy1sUCW9fUk18','https://www.openstreetmap.org/relation/304934',14);
INSERT INTO countries VALUES(107,'Ireland','Republic of Ireland','IE',70273.0,'.ie','🇮🇪',7185600,45,34,'https://goo.gl/maps/hxd1BKxgpchStzQC6','https://www.openstreetmap.org/relation/62273',17);
INSERT INTO countries VALUES(108,'Isle of Man','Isle of Man','IM',572.0,'.im','🇮🇲',84523,49,34,'https://goo.gl/maps/4DqVHDgVaFgnh8ZV8','https://www.openstreetmap.org/relation/62269',17);
INSERT INTO countries VALUES(109,'Israel','State of Israel','IL',20770.0,'.il','🇮🇱',10147200,63,5,'https://goo.gl/maps/6UY1AH8XeafVwdC97','https://www.openstreetmap.org/relation/1473946',14);
INSERT INTO countries VALUES(110,'Italy','Italian Republic','IT',301336.0,'.it','🇮🇹',58915561,45,60,'https://goo.gl/maps/8M1K27TDj7StTRTq8','https://www.openstreetmap.org/relation/365331',19);
INSERT INTO countries VALUES(111,'Ivory Coast','Republic of Côte d''Ivoire','CI',322463.0,'.ci','🇨🇮',31500000,158,41,'https://goo.gl/maps/wKsmN7f5qAeNtGjP6','https://www.openstreetmap.org/relation/192779',5);
INSERT INTO countries VALUES(112,'Jamaica','Jamaica','JM',10991.0,'.jm','🇯🇲',2824913,70,34,'https://goo.gl/maps/Z8mQ6jxnRQKFwJy9A','https://www.openstreetmap.org/relation/555017',6);
INSERT INTO countries VALUES(113,'Japan','Japan','JP',377930.0,'.jp','🇯🇵',122950000,72,62,'https://goo.gl/maps/NGTLSCSrA8bMrvnX9','https://www.openstreetmap.org/relation/382313',11);
INSERT INTO countries VALUES(114,'Jersey','Bailiwick of Jersey','JE',116.0,'.je','🇯🇪',104540,49,34,'https://goo.gl/maps/rXG8GZZtsqK92kTCA','https://www.openstreetmap.org/relation/367988',17);
INSERT INTO countries VALUES(115,'Jordan','Hashemite Kingdom of Jordan','JO',89342.0,'.jo','🇯🇴',11484805,71,5,'https://goo.gl/maps/ko1dzSDKg8Gsi9A98','https://www.openstreetmap.org/relation/184818',14);
INSERT INTO countries VALUES(116,'Kazakhstan','Republic of Kazakhstan','KZ',2724900.0,'.kz','🇰🇿',20547909,82,64,'https://goo.gl/maps/8VohJGu7ShuzZYyeA','https://www.openstreetmap.org/relation/214665',10);
INSERT INTO countries VALUES(117,'Kenya','Republic of Kenya','KE',580367.0,'.ke','🇰🇪',53330978,73,34,'https://goo.gl/maps/Ni9M7wcCxf8bJHLX8','https://www.openstreetmap.org/relation/192798',1);
INSERT INTO countries VALUES(118,'Kiribati','Independent and Sovereign Republic of Kiribati','KI',811.0,'.ki','🇰🇮',138000,8,34,'https://goo.gl/maps/NBfYvrndW4skAimw9','https://www.openstreetmap.org/relation/571178',23);
INSERT INTO countries VALUES(119,'Kosovo','Republic of Kosovo','XK',10908.0,'','🇽🇰',1585566,45,3,'https://goo.gl/maps/CSC4Yc8SWPgburuD9','https://www.openstreetmap.org/relation/2088990',18);
INSERT INTO countries VALUES(120,'Kuwait','State of Kuwait','KW',17818.0,'.kw','🇰🇼',4985716,80,5,'https://goo.gl/maps/aqr3aNQjS1BAvksJ7','https://www.openstreetmap.org/relation/305099',14);
INSERT INTO countries VALUES(121,'Kyrgyzstan','Kyrgyz Republic','KG',199951.0,'.kg','🇰🇬',7400000,74,71,'https://goo.gl/maps/SKG8BSMMQVvxkRkB7','https://www.openstreetmap.org/relation/178009',10);
INSERT INTO countries VALUES(122,'Laos','Lao People''s Democratic Republic','LA',236800.0,'.la','🇱🇦',6740000,83,72,'https://goo.gl/maps/F3asVB7sRKgSnwbE7','https://www.openstreetmap.org/relation/49903',12);
INSERT INTO countries VALUES(123,'Latvia','Republic of Latvia','LV',64559.0,'.lv','🇱🇻',1842226,45,74,'https://goo.gl/maps/iQpUkH7ghq31ZtXe9','https://www.openstreetmap.org/relation/72594',17);
INSERT INTO countries VALUES(124,'Lebanon','Lebanese Republic','LB',10452.0,'.lb','🇱🇧',5364482,84,5,'https://goo.gl/maps/Sz5VCU8UFBqMyTdc9','https://www.openstreetmap.org/relation/184843',14);
INSERT INTO countries VALUES(125,'Lesotho','Kingdom of Lesotho','LS',30355.0,'.ls','🇱🇸',2116427,87,34,'https://goo.gl/maps/H8gJi5mL4Cmd1SF28','https://www.openstreetmap.org/relation/2093234',4);
INSERT INTO countries VALUES(126,'Liberia','Republic of Liberia','LR',111369.0,'.lr','🇱🇷',5437249,86,34,'https://goo.gl/maps/4VsHsc2oeGeRL3wg6','https://www.openstreetmap.org/relation/192780',5);
INSERT INTO countries VALUES(127,'Libya','State of Libya','LY',1759540.0,'.ly','🇱🇾',7361263,88,5,'https://goo.gl/maps/eLgGnaQWcJEdYRMy5','https://www.openstreetmap.org/relation/192758',3);
INSERT INTO countries VALUES(128,'Liechtenstein','Principality of Liechtenstein','LI',160.0,'.li','🇱🇮',41237,28,44,'https://goo.gl/maps/KNuHeiJzAPodwM7y6','https://www.openstreetmap.org/relation/1155955',20);
INSERT INTO countries VALUES(129,'Lithuania','Republic of Lithuania','LT',65300.0,'.lt','🇱🇹',2897430,45,76,'https://goo.gl/maps/dd1s9rrLjrK2G8yY6','https://www.openstreetmap.org/relation/72596',17);
INSERT INTO countries VALUES(130,'Luxembourg','Grand Duchy of Luxembourg','LU',2586.0,'.lu','🇱🇺',692402,45,44,'https://goo.gl/maps/L6b2AgndgHprt2Ko9','https://www.openstreetmap.org/relation/2171347#map=10/49.8167/6.1335',20);
INSERT INTO countries VALUES(131,'Macau','Macao Special Administrative Region of the People''s Republic of China','MO',30.0,'.mo','🇲🇴',712651,95,112,'https://goo.gl/maps/whymRdk3dZFfAAs4A','https://www.openstreetmap.org/relation/1867188',11);
INSERT INTO countries VALUES(132,'Madagascar','Republic of Madagascar','MG',587041.0,'.mg','🇲🇬',31964956,91,41,'https://goo.gl/maps/AHQh2ABBaFW6Ngj26','https://www.openstreetmap.org/relation/447325',1);
INSERT INTO countries VALUES(133,'Malawi','Republic of Malawi','MW',118484.0,'.mw','🇲🇼',21240689,99,34,'https://goo.gl/maps/mc6z83pW9m98X2Ef6','https://www.openstreetmap.org/relation/195290',1);
INSERT INTO countries VALUES(134,'Malaysia','Malaysia','MY',330803.0,'.my','🇲🇾',34564810,101,34,'https://goo.gl/maps/qrY1PNeUXGyXDcPy6','https://www.openstreetmap.org/relation/2108121',12);
INSERT INTO countries VALUES(135,'Maldives','Republic of Maldives','MV',300.0,'.mv','🇲🇻',601269,98,31,'https://goo.gl/maps/MNAWGq9vEdbZ9vUV7','https://www.openstreetmap.org/relation/536773',13);
INSERT INTO countries VALUES(136,'Mali','Republic of Mali','ML',1240192.0,'.ml','🇲🇱',25200000,158,41,'https://goo.gl/maps/u9mYJkCB19wyuzh27','https://www.openstreetmap.org/relation/192785',5);
INSERT INTO countries VALUES(137,'Malta','Republic of Malta','MT',316.0,'.mt','🇲🇹',519562,45,34,'https://goo.gl/maps/skXCqguxDxxEKVk47','https://www.openstreetmap.org/relation/365307',19);
INSERT INTO countries VALUES(138,'Marshall Islands','Republic of the Marshall Islands','MH',181.0,'.mh','🇲🇭',37548,149,34,'https://goo.gl/maps/A4xLi1XvcX88gi3W8','https://www.openstreetmap.org/relation/571771',23);
INSERT INTO countries VALUES(139,'Martinique','Martinique','MQ',1128.0,'.mq','🇲🇶',378243,45,41,'https://goo.gl/maps/87ER7sDAFU7JjcvR6','https://www.openstreetmap.org/relation/2473088',6);
INSERT INTO countries VALUES(140,'Mauritania','Islamic Republic of Mauritania','MR',1030700.0,'.mr','🇲🇷',5461319,96,5,'https://goo.gl/maps/im2MmQ5jFjzxWBks5','https://www.openstreetmap.org/relation/192763',5);
INSERT INTO countries VALUES(141,'Mauritius','Republic of Mauritius','MU',2040.0,'.mu','🇲🇺',1235260,97,34,'https://goo.gl/maps/PpKtZ4W3tir5iGrz7','https://www.openstreetmap.org/relation/535828',1);
INSERT INTO countries VALUES(142,'Mayotte','Department of Mayotte','YT',374.0,'.yt','🇾🇹',226915,45,41,'https://goo.gl/maps/1e7MXmfBwQv3TQGF7','https://www.openstreetmap.org/relation/1259885',1);
INSERT INTO countries VALUES(143,'Mexico','United Mexican States','MX',1964375.0,'.mx','🇲🇽',134407258,100,130,'https://goo.gl/maps/s5g7imNPMDEePxzbA','https://www.openstreetmap.org/relation/114686',8);
INSERT INTO countries VALUES(144,'Micronesia','Federated States of Micronesia','FM',702.0,'.fm','🇫🇲',75817,149,34,'https://goo.gl/maps/LLcnofC5LxZsJXTo8','https://www.openstreetmap.org/relation/571802',23);
INSERT INTO countries VALUES(145,'Moldova','Republic of Moldova','MD',33846.0,'.md','🇲🇩',2381325,90,114,'https://goo.gl/maps/JjmyUuULujnDeFPf7','https://www.openstreetmap.org/relation/58974',16);
INSERT INTO countries VALUES(146,'Monaco','Principality of Monaco','MC',2.02,'.mc','🇲🇨',38857,45,41,'https://goo.gl/maps/DGpndDot28bYdXYn7','https://www.openstreetmap.org/relation/1124039',20);
INSERT INTO countries VALUES(147,'Mongolia','Mongolia','MN',1564110.0,'.mn','🇲🇳',3591120,94,89,'https://goo.gl/maps/A1X7bMCKThBDNjzH6','https://www.openstreetmap.org/relation/161033',11);
INSERT INTO countries VALUES(148,'Montenegro','Montenegro','ME',13812.0,'.me','🇲🇪',622902,45,90,'https://goo.gl/maps/4THX1fM7WqANuPbB8','https://www.openstreetmap.org/relation/53296',18);
INSERT INTO countries VALUES(149,'Montserrat','Montserrat','MS',102.0,'.ms','🇲🇸',4399,157,34,'https://goo.gl/maps/CSbe7UmxPmiwQB7GA','https://www.openstreetmap.org/relation/537257',6);
INSERT INTO countries VALUES(150,'Morocco','Kingdom of Morocco','MA',446550.0,'.ma','🇲🇦',36828330,89,5,'https://goo.gl/maps/6oMv3dyBZg3iaXQ5A','https://www.openstreetmap.org/relation/3630439',3);
INSERT INTO countries VALUES(151,'Mozambique','Republic of Mozambique','MZ',801590.0,'.mz','🇲🇿',34881007,102,112,'https://goo.gl/maps/xCLcY9fzU6x4Pueu5','https://www.openstreetmap.org/relation/195273',1);
INSERT INTO countries VALUES(152,'Myanmar','Republic of the Union of Myanmar','MM',676578.0,'.mm','🇲🇲',55770232,93,19,'https://goo.gl/maps/4jrZyJkDERUfHyp26','https://www.openstreetmap.org/relation/50371',12);
INSERT INTO countries VALUES(153,'Namibia','Republic of Namibia','NA',825615.0,'.na','🇳🇦',3022401,103,2,'https://goo.gl/maps/oR1i8BFEYX3EY83WA','https://www.openstreetmap.org/relation/195266',4);
INSERT INTO countries VALUES(154,'Nauru','Republic of Nauru','NR',21.0,'.nr','🇳🇷',12025,8,34,'https://goo.gl/maps/kyAGw6XEJgjSMsTK7','https://www.openstreetmap.org/relation/571804',23);
INSERT INTO countries VALUES(155,'Nepal','Federal Democratic Republic of Nepal','NP',147181.0,'.np','🇳🇵',31122387,107,94,'https://goo.gl/maps/UMj2zpbQp7B5c3yT7','https://www.openstreetmap.org/relation/184633',13);
INSERT INTO countries VALUES(156,'Netherlands','Kingdom of the Netherlands','NL',41850.0,'.nl','🇳🇱',18044027,45,32,'https://goo.gl/maps/Hv6zQswGhFxoVVBm6','https://www.openstreetmap.org/relation/47796',20);
INSERT INTO countries VALUES(157,'New Caledonia','New Caledonia','NC',18575.0,'.nc','🇳🇨',264596,159,41,'https://goo.gl/maps/cBhtCeMdob4U7FRU9','https://www.openstreetmap.org/relation/3407643',22);
INSERT INTO countries VALUES(158,'New Zealand','New Zealand','NZ',270467.0,'.nz','🇳🇿',4993923,108,34,'https://goo.gl/maps/xXiDQo65dwdpw9iu8','https://www.openstreetmap.org/relation/556706#map=5/-46.710/172.046',21);
INSERT INTO countries VALUES(159,'Nicaragua','Republic of Nicaragua','NI',130373.0,'.ni','🇳🇮',6676948,105,130,'https://goo.gl/maps/P77LaEVkKJKXneRC6','https://www.openstreetmap.org/relation/287666',7);
INSERT INTO countries VALUES(160,'Niger','Republic of Niger','NE',1267000.0,'.ne','🇳🇪',26342784,158,41,'https://goo.gl/maps/VKNU2TLsZcgxM49c8','https://www.openstreetmap.org/relation/192786',5);
INSERT INTO countries VALUES(161,'Nigeria','Federal Republic of Nigeria','NG',923768.0,'.ng','🇳🇬',242747130,104,34,'https://goo.gl/maps/LTn417qWwBPFszuV9','https://www.openstreetmap.org/relation/192787',5);
INSERT INTO countries VALUES(162,'Niue','Niue','NU',260.0,'.nu','🇳🇺',1681,108,34,'https://goo.gl/maps/xFgdzs3E55Rk1y8P9','https://www.openstreetmap.org/relation/1558556',24);
INSERT INTO countries VALUES(163,'Norfolk Island','Territory of Norfolk Island','NF',36.0,'.nf','🇳🇫',2188,8,34,'https://goo.gl/maps/pbvtm6XYd1iZbjky5','https://www.openstreetmap.org/relation/2574988',21);
INSERT INTO countries VALUES(164,'North Korea','Democratic People''s Republic of Korea','KP',120538.0,'.kp','🇰🇵',25950000,78,69,'https://goo.gl/maps/9q5T2DMeH5JL7Tky6','https://www.openstreetmap.org/relation/192734',11);
INSERT INTO countries VALUES(165,'North Macedonia','Republic of North Macedonia','MK',25713.0,'.mk','🇲🇰',1836713,92,81,'https://goo.gl/maps/55Q8MEnF6ACdu3q79','https://www.openstreetmap.org/relation/53293',18);
INSERT INTO countries VALUES(166,'Northern Cyprus','Turkish Republic of Northern Cyprus','',3355.0,'','',382836,142,147,'','',19);
INSERT INTO countries VALUES(167,'Northern Mariana Islands','Commonwealth of the Northern Mariana Islands','MP',464.0,'.mp','🇲🇵',46078,149,20,'https://goo.gl/maps/cpZ67knoRAcfu1417','https://www.openstreetmap.org/relation/306004',23);
INSERT INTO countries VALUES(168,'Norway','Kingdom of Norway','NO',323802.0,'.no','🇳🇴',5627400,106,105,'https://goo.gl/maps/htWRrphA7vNgQNdSA','https://www.openstreetmap.org/relation/2978650',17);
INSERT INTO countries VALUES(169,'Oman','Sultanate of Oman','OM',309500.0,'.om','🇴🇲',5494691,109,5,'https://goo.gl/maps/L2BoXoAwDDwWecnw5','https://www.openstreetmap.org/relation/305138',14);
INSERT INTO countries VALUES(170,'Pakistan','Islamic Republic of Pakistan','PK',881912.0,'.pk','🇵🇰',241499431,114,34,'https://goo.gl/maps/5LYujdfR5yLUXoERA','https://www.openstreetmap.org/relation/307573',13);
INSERT INTO countries VALUES(171,'Palau','Republic of Palau','PW',459.0,'.pw','🇵🇼',17663,149,34,'https://goo.gl/maps/MVasQBbUkQP7qQDR9','https://www.openstreetmap.org/relation/571805',23);
INSERT INTO countries VALUES(172,'Palestine','State of Palestine','PS',6220.0,'.ps','🇵🇸',5483450,42,5,'https://goo.gl/maps/QvTbkRdmdWEoYAmt5','https://www.openstreetmap.org/relation/1703814',14);
INSERT INTO countries VALUES(173,'Panama','Republic of Panama','PA',75417.0,'.pa','🇵🇦',4337768,110,130,'https://goo.gl/maps/sEN7sKqeawa5oPNLA','https://www.openstreetmap.org/relation/287668',7);
INSERT INTO countries VALUES(174,'Papua New Guinea','Independent State of Papua New Guinea','PG',462840.0,'.pg','🇵🇬',11781559,112,34,'https://goo.gl/maps/ChGmzZBjZ3vnBwR2A','https://www.openstreetmap.org/relation/307866',22);
INSERT INTO countries VALUES(175,'Paraguay','Republic of Paraguay','PY',406752.0,'.py','🇵🇾',6460159,116,48,'https://goo.gl/maps/JtnqG73WJn1Gx6mz6','https://www.openstreetmap.org/relation/287077',9);
INSERT INTO countries VALUES(176,'Peru','Republic of Peru','PE',1285216.0,'.pe','🇵🇪',34352720,111,9,'https://goo.gl/maps/uDWEUaXNcZTng1fP6','https://www.openstreetmap.org/relation/288247',9);
INSERT INTO countries VALUES(177,'Philippines','Republic of the Philippines','PH',342353.0,'.ph','🇵🇭',112729484,113,34,'https://goo.gl/maps/k8T2fb5VMUfsWFX6A','https://www.openstreetmap.org/relation/443174',12);
INSERT INTO countries VALUES(178,'Pitcairn Islands','Pitcairn Group of Islands','PN',47.0,'.pn','🇵🇳',35,108,34,'https://goo.gl/maps/XGJMnMAigXjXcxSa7','https://www.openstreetmap.org/relation/2185375',24);
INSERT INTO countries VALUES(179,'Poland','Republic of Poland','PL',312679.0,'.pl','🇵🇱',37314000,115,111,'https://goo.gl/maps/gY9Xw4Sf4415P4949','https://www.openstreetmap.org/relation/49715',15);
INSERT INTO countries VALUES(180,'Portugal','Portuguese Republic','PT',92090.0,'.pt','🇵🇹',10749635,45,112,'https://goo.gl/maps/BaTBSyc4GWMmbAKB8','https://www.openstreetmap.org/relation/295480',19);
INSERT INTO countries VALUES(181,'Puerto Rico','Commonwealth of Puerto Rico','PR',8870.0,'.pr','🇵🇷',3194034,149,34,'https://goo.gl/maps/sygfDbtwn389wu8x5','https://www.openstreetmap.org/relation/4422604',6);
INSERT INTO countries VALUES(182,'Qatar','State of Qatar','QA',11586.0,'.qa','🇶🇦',3214609,117,5,'https://goo.gl/maps/ZV76Y49z7LLUZ2KQ6','https://www.openstreetmap.org/relation/305095',14);
INSERT INTO countries VALUES(183,'Romania','Romania','RO',238391.0,'.ro','🇷🇴',19043151,118,114,'https://goo.gl/maps/845hAgCf1mDkN3vr7','https://www.openstreetmap.org/relation/90689',18);
INSERT INTO countries VALUES(184,'Russia','Russian Federation','RU',17098242.0,'.ru','🇷🇺',146028325,120,117,'https://goo.gl/maps/4F4PpDhGJgVvLby57','https://www.openstreetmap.org/relation/60189#map=3/65.15/105.29',16);
INSERT INTO countries VALUES(185,'Rwanda','Republic of Rwanda','RW',26338.0,'.rw','🇷🇼',14104969,121,34,'https://goo.gl/maps/j5xb5r7CLqjYbyP86','https://www.openstreetmap.org/relation/171496',1);
INSERT INTO countries VALUES(186,'Réunion','Réunion Island','RE',2511.0,'.re','🇷🇪',840974,45,41,'https://goo.gl/maps/wWpBrXsp8UHVbah29','https://www.openstreetmap.org/relation/1785276',1);
INSERT INTO countries VALUES(187,'Saint Barthélemy','Collectivity of Saint Barthélemy','BL',21.0,'.bl','🇧🇱',4255,45,41,'https://goo.gl/maps/Mc7GqH466S7AAk297','https://www.openstreetmap.org/relation/7552779',6);
INSERT INTO countries VALUES(188,'Saint Helena, Ascension and Tristan da Cunha','Saint Helena, Ascension and Tristan da Cunha','SH',394.0,'.sh','🇸🇭',53192,49,34,'https://goo.gl/maps/iv4VxnPzHkjLCJuc6','https://www.openstreetmap.org/relation/4868269#map=13/-15.9657/-5.7120',5);
INSERT INTO countries VALUES(189,'Saint Kitts and Nevis','Federation of Saint Christopher and Nevis','KN',261.0,'.kn','🇰🇳',54338,157,34,'https://goo.gl/maps/qiaVwcLVTXX3eoTNA','https://www.openstreetmap.org/relation/536899',6);
INSERT INTO countries VALUES(190,'Saint Lucia','Saint Lucia','LC',616.0,'.lc','🇱🇨',184100,157,34,'https://goo.gl/maps/4HhJ2jkPdSL9BPRcA','https://www.openstreetmap.org/relation/550728',6);
INSERT INTO countries VALUES(191,'Saint Martin','Saint Martin','MF',53.0,'.fr','🇲🇫',38659,45,41,'https://goo.gl/maps/P9ho9QuJ9EAR28JEA','https://www.openstreetmap.org/relation/63064',6);
INSERT INTO countries VALUES(192,'Saint Pierre and Miquelon','Saint Pierre and Miquelon','PM',242.0,'.pm','🇵🇲',5819,45,41,'https://goo.gl/maps/bUM8Yc8pA8ghyhmt6','https://www.openstreetmap.org/relation/3406826',8);
INSERT INTO countries VALUES(193,'Saint Vincent and the Grenadines','Saint Vincent and the Grenadines','VC',389.0,'.vc','🇻🇨',110872,157,34,'https://goo.gl/maps/wMbnMqjG37FMnrwf7','https://www.openstreetmap.org/relation/550725',6);
INSERT INTO countries VALUES(194,'Samoa','Independent State of Samoa','WS',2842.0,'.ws','🇼🇸',205557,155,34,'https://goo.gl/maps/CFC9fEFP9cfkYUBF9','https://www.openstreetmap.org/relation/1872673',24);
INSERT INTO countries VALUES(195,'San Marino','Republic of San Marino','SM',61.0,'.sm','🇸🇲',34172,45,60,'https://goo.gl/maps/rxCVJjm8dVY93RPY8','https://www.openstreetmap.org/relation/54624',19);
INSERT INTO countries VALUES(196,'Saudi Arabia','Kingdom of Saudi Arabia','SA',2149690.0,'.sa','🇸🇦',33702731,122,5,'https://goo.gl/maps/5PSjvdJ1AyaLFRrG9','https://www.openstreetmap.org/relation/307584',14);
INSERT INTO countries VALUES(197,'Senegal','Republic of Senegal','SN',196722.0,'.sn','🇸🇳',18847519,158,41,'https://goo.gl/maps/o5f1uD5nyihCL3HCA','https://www.openstreetmap.org/relation/192775',5);
INSERT INTO countries VALUES(198,'Serbia','Republic of Serbia','RS',88361.0,'.rs','🇷🇸',6567783,119,120,'https://goo.gl/maps/2Aqof7aV2Naq8YEK8','https://www.openstreetmap.org/relation/1741311',18);
INSERT INTO countries VALUES(199,'Seychelles','Republic of Seychelles','SC',452.0,'.sc','🇸🇨',121355,124,121,'https://goo.gl/maps/aqCcy2TKh5TV5MAX8','https://www.openstreetmap.org/relation/536765',1);
INSERT INTO countries VALUES(200,'Sierra Leone','Republic of Sierra Leone','SL',71740.0,'.sl','🇸🇱',8460512,129,34,'https://goo.gl/maps/jhacar85oq9QaeKB7','https://www.openstreetmap.org/relation/192777',5);
INSERT INTO countries VALUES(201,'Singapore','Republic of Singapore','SG',710.0,'.sg','🇸🇬',6110200,127,34,'https://goo.gl/maps/QbQt9Y9b5KFzsahV6','https://www.openstreetmap.org/relation/536780',12);
INSERT INTO countries VALUES(202,'Sint Maarten','Sint Maarten','SX',34.0,'.sx','🇸🇽',58477,5,34,'https://goo.gl/maps/DjvcESy1a1oGEZuNA','https://www.openstreetmap.org/relation/1231790',6);
INSERT INTO countries VALUES(203,'Slovakia','Slovak Republic','SK',49037.0,'.sk','🇸🇰',5405368,45,124,'https://goo.gl/maps/uNSH2wW4bLoZVYJj7','https://www.openstreetmap.org/relation/14296',15);
INSERT INTO countries VALUES(204,'Slovenia','Republic of Slovenia','SI',20273.0,'.si','🇸🇮',2135107,45,125,'https://goo.gl/maps/7zgFmswcCJh5L5D49','https://www.openstreetmap.org/relation/218657',15);
INSERT INTO countries VALUES(205,'Solomon Islands','Solomon Islands','SB',28896.0,'.sb','🇸🇧',828857,123,34,'https://goo.gl/maps/JbPkx86Ywjv8C1n8A','https://www.openstreetmap.org/relation/1857436',22);
INSERT INTO countries VALUES(206,'Somalia','Federal Republic of Somalia','SO',637657.0,'.so','🇸🇴',19280850,131,5,'https://goo.gl/maps/8of8q7D1a8p7R6Fc9','https://www.openstreetmap.org/relation/192799',1);
INSERT INTO countries VALUES(207,'Somaliland','Republic of Somaliland','',137600.0,'','',6200000,130,126,'','',1);
INSERT INTO countries VALUES(208,'South Africa','Republic of South Africa','ZA',1221037.0,'.za','🇿🇦',63015904,161,2,'https://goo.gl/maps/CLCZ1R8Uz1KpYhRv6','https://www.openstreetmap.org/relation/87565',4);
INSERT INTO countries VALUES(209,'South Georgia','South Georgia and the South Sandwich Islands','GS',3903.0,'.gs','🇬🇸',32,49,34,'https://goo.gl/maps/mJzdaBwKBbm2B81q9','https://www.openstreetmap.org/relation/1983629',NULL);
INSERT INTO countries VALUES(210,'South Korea','Republic of Korea','KR',100210.0,'.kr','🇰🇷',51106229,79,69,'https://goo.gl/maps/7ecjaJXefjAQhxjGA','https://www.openstreetmap.org/relation/307756',11);
INSERT INTO countries VALUES(211,'South Ossetia','Republic of South Ossetia','',3900.0,'','',56520,120,106,'','',14);
INSERT INTO countries VALUES(212,'South Sudan','Republic of South Sudan','SS',619745.0,'.ss','🇸🇸',12703714,133,34,'https://goo.gl/maps/Zm1AYCXb9HSNF1P27','https://www.openstreetmap.org/relation/1656678',2);
INSERT INTO countries VALUES(213,'Spain','Kingdom of Spain','ES',505992.0,'.es','🇪🇸',49687120,45,130,'https://goo.gl/maps/138JaXW8EZzRVitY9','https://www.openstreetmap.org/relation/1311341',19);
INSERT INTO countries VALUES(214,'Sri Lanka','Democratic Socialist Republic of Sri Lanka','LK',65610.0,'.lk','🇱🇰',21756000,85,123,'https://goo.gl/maps/VkPHoeFSfgzRQCDv8','https://www.openstreetmap.org/relation/536807',13);
INSERT INTO countries VALUES(215,'Sudan','Republic of the Sudan','SD',1886068.0,'.sd','🇸🇩',51767437,125,5,'https://goo.gl/maps/bNW7YUJCaqR8zcXn7','https://www.openstreetmap.org/relation/192789',3);
INSERT INTO countries VALUES(216,'Suriname','Republic of Suriname','SR',163820.0,'.sr','🇸🇷',632638,132,32,'https://goo.gl/maps/iy7TuQLSi4qgoBoG7','https://www.openstreetmap.org/relation/287082',9);
INSERT INTO countries VALUES(217,'Svalbard and Jan Mayen','Svalbard og Jan Mayen','SJ',61399.0,'.sj','🇸🇯',2562,106,103,'https://goo.gl/maps/L2wyyn3cQ16PzQ5J8','https://www.openstreetmap.org/relation/1337397',17);
INSERT INTO countries VALUES(218,'Sweden','Kingdom of Sweden','SE',450295.0,'.se','🇸🇪',10610485,126,134,'https://goo.gl/maps/iqygE491ADVgnBW39','https://www.openstreetmap.org/relation/52822',17);
INSERT INTO countries VALUES(219,'Switzerland','Swiss Confederation','CH',41284.0,'.ch','🇨🇭',9060598,28,41,'https://goo.gl/maps/uVuZcXaxSx5jLyEC9','https://www.openstreetmap.org/relation/51701',20);
INSERT INTO countries VALUES(220,'Syria','Syrian Arab Republic','SY',185180.0,'.sy','🇸🇾',26019711,135,5,'https://goo.gl/maps/Xe3VnFbwdb4nv2SM9','https://www.openstreetmap.org/relation/184840',14);
INSERT INTO countries VALUES(221,'São Tomé and Príncipe','Democratic Republic of São Tomé and Príncipe','ST',964.0,'.st','🇸🇹',220372,134,112,'https://goo.gl/maps/9EUppm13RtPX9oF46','https://www.openstreetmap.org/relation/535880',2);
INSERT INTO countries VALUES(222,'Taiwan','Republic of China (Taiwan)','TW',36193.0,'.tw','🇹🇼',23299132,145,25,'https://goo.gl/maps/HgMKFQjNadF3Wa6B6','https://www.openstreetmap.org/relation/449220',11);
INSERT INTO countries VALUES(223,'Tajikistan','Republic of Tajikistan','TJ',143100.0,'.tj','🇹🇯',10786734,138,117,'https://goo.gl/maps/8rQgW88jEXijhVb58','https://www.openstreetmap.org/relation/214626',10);
INSERT INTO countries VALUES(224,'Tanzania','United Republic of Tanzania','TZ',945087.0,'.tz','🇹🇿',67462121,146,34,'https://goo.gl/maps/NWYMqZYXte4zGZ2Q8','https://www.openstreetmap.org/relation/195270',1);
INSERT INTO countries VALUES(225,'Thailand','Kingdom of Thailand','TH',513120.0,'.th','🇹🇭',65975198,137,139,'https://goo.gl/maps/qeU6uqsfW4nCCwzw9','https://www.openstreetmap.org/relation/2067731',12);
INSERT INTO countries VALUES(226,'Timor-Leste','Democratic Republic of Timor-Leste','TL',14874.0,'.tl','🇹🇱',1434991,149,112,'https://goo.gl/maps/sFqBC9zjgUXPR1iTA','https://www.openstreetmap.org/relation/305142',12);
INSERT INTO countries VALUES(227,'Togo','Togolese Republic','TG',56785.0,'.tg','🇹🇬',9583381,158,41,'https://goo.gl/maps/jzAa9feXuXPrKVb89','https://www.openstreetmap.org/relation/192782',5);
INSERT INTO countries VALUES(228,'Tokelau','Tokelau','TK',12.0,'.tk','🇹🇰',1411,108,34,'https://goo.gl/maps/Ap5qN8qien6pT9UN6','https://www.openstreetmap.org/relation/2186600',24);
INSERT INTO countries VALUES(229,'Tonga','Kingdom of Tonga','TO',747.0,'.to','🇹🇴',100179,141,34,'https://goo.gl/maps/p5YALBY2QdEzswRo7','https://www.openstreetmap.org/relation/2186665',24);
INSERT INTO countries VALUES(230,'Trinidad and Tobago','Republic of Trinidad and Tobago','TT',5130.0,'.tt','🇹🇹',1512779,143,34,'https://goo.gl/maps/NrRfDEWoG8FGZqWY7','https://www.openstreetmap.org/relation/555717',6);
INSERT INTO countries VALUES(231,'Tunisia','Republic of Tunisia','TN',163610.0,'.tn','🇹🇳',11972169,140,5,'https://goo.gl/maps/KgUmpZdUuNRaougs8','https://www.openstreetmap.org/relation/192757',3);
INSERT INTO countries VALUES(232,'Turkey','Republic of Türkiye','TR',783562.0,'.tr','🇹🇷',86092168,142,147,'https://goo.gl/maps/dXFFraiUDfcB6Quk6','https://www.openstreetmap.org/relation/174737',14);
INSERT INTO countries VALUES(233,'Turkmenistan','Turkmenistan','TM',488100.0,'.tm','🇹🇲',7057841,139,117,'https://goo.gl/maps/cgfUcaQHSWKuqeKk9','https://www.openstreetmap.org/relation/223026',10);
INSERT INTO countries VALUES(234,'Turks and Caicos Islands','Turks and Caicos Islands','TC',948.0,'.tc','🇹🇨',50828,149,34,'https://goo.gl/maps/R8VUDQfwZiFtvmyn8','https://www.openstreetmap.org/relation/547479',6);
INSERT INTO countries VALUES(235,'Tuvalu','Tuvalu','TV',26.0,'.tv','🇹🇻',10643,8,34,'https://goo.gl/maps/LbuUxtkgm1dfN1Pn6','https://www.openstreetmap.org/relation/2177266',24);
INSERT INTO countries VALUES(236,'Uganda','Republic of Uganda','UG',241550.0,'.ug','🇺🇬',45905417,148,34,'https://goo.gl/maps/Y7812hFiGa8LD9N68','https://www.openstreetmap.org/relation/192796',1);
INSERT INTO countries VALUES(237,'Ukraine','Ukraine','UA',603500.0,'.ua','🇺🇦',32283000,147,150,'https://goo.gl/maps/DvgJMiPJ7aozKFZv7','https://www.openstreetmap.org/relation/60199',16);
INSERT INTO countries VALUES(238,'United Arab Emirates','United Arab Emirates','AE',83600.0,'.ae','🇦🇪',11027129,1,5,'https://goo.gl/maps/AZZTDA6GzVAnKMVd8','https://www.openstreetmap.org/relation/307763',14);
INSERT INTO countries VALUES(239,'United Kingdom','United Kingdom of Great Britain and Northern Ireland','GB',242900.0,'.uk','🇬🇧',66912637,49,34,'https://goo.gl/maps/FoDtc3UKMkFsXAjHA','https://www.openstreetmap.org/relation/62149',17);
INSERT INTO countries VALUES(240,'United States','United States of America','US',9372610.0,'.us','🇺🇸',341784857,149,34,'https://goo.gl/maps/e8M246zY4BSjkjAv6','https://www.openstreetmap.org/relation/148838#map=2/20.6/-85.8',8);
INSERT INTO countries VALUES(241,'United States Minor Outlying Islands','United States Minor Outlying Islands','UM',34.2,'.us','🇺🇲',300,149,34,'https://goo.gl/maps/hZKnrzgeK69dDyPF8','https://www.openstreetmap.org/relation/6430384',8);
INSERT INTO countries VALUES(242,'United States Virgin Islands','Virgin Islands of the United States','VI',347.0,'.vi','🇻🇮',87146,149,34,'https://goo.gl/maps/mBfreywj8dor6q4m9','https://www.openstreetmap.org/relation/286898',6);
INSERT INTO countries VALUES(243,'Uruguay','Oriental Republic of Uruguay','UY',181034.0,'.uy','🇺🇾',3499451,150,130,'https://goo.gl/maps/tiQ9Baekb1jQtDSD9','https://www.openstreetmap.org/relation/287072',9);
INSERT INTO countries VALUES(244,'Uzbekistan','Republic of Uzbekistan','UZ',447400.0,'.uz','🇺🇿',38236704,151,117,'https://goo.gl/maps/AJpo6MjMx23qSWCz8','https://www.openstreetmap.org/relation/196240',10);
INSERT INTO countries VALUES(245,'Vanuatu','Republic of Vanuatu','VU',12189.0,'.vu','🇻🇺',335908,154,16,'https://goo.gl/maps/hwAjehcT7VfvP5zJ8','https://www.openstreetmap.org/relation/2177246',22);
INSERT INTO countries VALUES(246,'Vatican City','Vatican City State','VA',0.44,'.va','🇻🇦',882,45,60,'https://goo.gl/maps/DTKvw5Bd1QZaDZmE8','https://www.openstreetmap.org/relation/36989',19);
INSERT INTO countries VALUES(247,'Venezuela','Bolivarian Republic of Venezuela','VE',916445.0,'.ve','🇻🇪',31800000,152,130,'https://goo.gl/maps/KLCwDN8sec7z2kse9','https://www.openstreetmap.org/relation/272644',9);
INSERT INTO countries VALUES(248,'Vietnam','Socialist Republic of Vietnam','VN',331212.0,'.vn','🇻🇳',102300000,153,155,'https://goo.gl/maps/PCpVt9WzdJ9A9nEZ9','https://www.openstreetmap.org/relation/49915',12);
INSERT INTO countries VALUES(249,'Wallis and Futuna','Territory of the Wallis and Futuna Islands','WF',142.0,'.wf','🇼🇫',11151,159,41,'https://goo.gl/maps/CzVqK74QYtbHv65r5','https://www.openstreetmap.org/relation/3412448',24);
INSERT INTO countries VALUES(250,'Western Sahara','Sahrawi Arab Democratic Republic','EH',266000.0,'.eh','🇪🇭',510713,41,51,'https://goo.gl/maps/7nU3mB69vP6zQp7A8','https://www.openstreetmap.org/relation/5441968',3);
INSERT INTO countries VALUES(251,'Yemen','Republic of Yemen','YE',527968.0,'.ye','🇾🇪',32684503,160,5,'https://goo.gl/maps/WCmE76HKcLideQQw7','https://www.openstreetmap.org/relation/305092',14);
INSERT INTO countries VALUES(252,'Zambia','Republic of Zambia','ZM',752612.0,'.zm','🇿🇲',20216029,162,34,'https://goo.gl/maps/mweBcqvW8TppZW6q9','https://www.openstreetmap.org/relation/195271',1);
INSERT INTO countries VALUES(253,'Zimbabwe','Republic of Zimbabwe','ZW',390757.0,'.zw','🇿🇼',17166852,163,11,'https://goo.gl/maps/M26BqdwQctqxXS65A','https://www.openstreetmap.org/relation/195272',4);
INSERT INTO countries VALUES(254,'Åland Islands','Åland Islands','AX',1580.0,'.ax','🇦🇽',30654,45,134,'https://goo.gl/maps/ewFb3vYsfUmVCoSb8','https://www.openstreetmap.org/relation/1650407',17);
CREATE TABLE locations (
	location_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	latitude REAL NOT NULL, 
	longitude REAL NOT NULL, 
	elevation REAL NOT NULL, 
	population INTEGER NOT NULL, 
	timezone VARCHAR(255) DEFAULT UTC NOT NULL, 
	country_id INTEGER NOT NULL, 
	PRIMARY KEY (location_id), 
	UNIQUE (name), 
	FOREIGN KEY(country_id) REFERENCES countries (country_id) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE TABLE users (
	user_id INTEGER NOT NULL, 
	username VARCHAR(255) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	home_location_id INTEGER DEFAULT null, 
	PRIMARY KEY (user_id), 
	UNIQUE (username), 
	UNIQUE (email), 
	FOREIGN KEY(home_location_id) REFERENCES locations (location_id) ON DELETE RESTRICT ON UPDATE CASCADE
);
COMMIT;
