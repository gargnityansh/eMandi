-------------------------
--USER DETAIL INSERTION--
-------------------------
--uid, fn, ln, ph, email, pass, type
/*insert into User_Details values ('9385', 'lrbbmqbh', 'darz', '7513928', 'kk', crypt('hi', gen_salt('bf')), default);
insert into User_Details values ('2569', 'qscdxrjmowf', 'xsjybldbe', '6898539', 'arcbynecdyggxxpklore', crypt('lnm', gen_salt('bf')), default);
insert into User_Details values ('3897', 'pqfw', 'hopkmc', '695790', 'hnwnku', crypt('whsqmg', gen_salt('bf')), default);
insert into User_Details values ('7541', 'uqcljji', 'swmdkqtbx', '4228446', 'mvtrrbljptnsnfwzqfjma', crypt('adrrwsofs', gen_salt('bf')), default);
insert into User_Details values ('8151', 'nuvqhffb', 'aqxwpqcace', '8936989', 'hzvfrkmlnozjkpqpxr', crypt('xkitz', gen_salt('bf')), default);
insert into User_Details values ('5930', 'acbhhkicqco', 'ndtomfgdwd', '6689774', 'cgpxiqv', crypt('uytd', gen_salt('bf')), default);
insert into User_Details values ('9357', 'gdewht', 'ciohordt', '6473732', 'vwcsgspqoqmsboaguwnn', crypt('qxnzlgdg', gen_salt('bf')), default);
insert into User_Details values ('8662', 'btrwb', 'nsade', '7116468', 'uumoqc', crypt('rubet', gen_salt('bf')), default);
insert into User_Details values ('9414', 'yxhoachwdv', 'xxrd', '7517723', 'xlmndq', crypt('ukwagmlej', gen_salt('bf')), default);
insert into User_Details values ('5632', 'kwcibx', 'bume', '6340715', 'eyatdrmydiajxloghiqf', crypt('zhlvih', gen_salt('bf')), default);
insert into User_Details values ('1963', 'uvsuyo', 'payuly', '7949910', 'muotehzriicfskpggkbb', crypt('pzzrzucx', gen_salt('bf')), default);
insert into User_Details values ('1154', 'ludfykgr', 'ow', '8388029', 'iooobppleqlw', crypt('hap', gen_salt('bf')), default);
insert into User_Details values ('5153', 'adqhdcn', 'wdtxjbmyppp', '5495369', 'uxnspusgdh', crypt('ixqm', gen_salt('bf')), default);
insert into User_Details values ('9119', 'jxjcv', 'djsuyiby', '6673170', 'mwsiqyo', crypt('gyxymz', gen_salt('bf')), default);
insert into User_Details values ('6972', 'ypz', 'jegebeocf', '1909612', 'tsxdixtigsi', crypt('ehkchz', gen_salt('bf')), default);
insert into User_Details values ('7207', 'lilrjqfnxzt', 'rsvbspkyhs', '4633076', 'bppkqtpddbuotbb', crypt('cwivrfxj', gen_salt('bf')), default);
insert into User_Details values ('8576', 'jdd', 'tge', '3614032', 'vdgaijvwcyaubwewpjvy', crypt('eh', gen_salt('bf')), default);
insert into User_Details values ('9209', 'xepbpiwuqzd', 'ubdubzvafsp', '9544920', 'qwuzifw', crypt('vyddwyvv', gen_salt('bf')), default);
insert into User_Details values ('8379', 'rczm', 'yjgf', '7871139', 'vtnunneslsplw', crypt('iupf', gen_salt('bf')), default);
insert into User_Details values ('9635', 'zbknhkw', 'panlt', '7721122', 'irjcddsoz', crypt('yveg', gen_salt('bf')), default);*/
---------------------
--IDENTTY INSERTION--
---------------------
--name, release, id
insert into Identty values('Cyberpunk 2077', '2020/12/01', 'Cyberpunk 2077_2020/12/01');
insert into Identty values('Red Dead Online', '2020/12/02', 'Red Dead Online_2020/12/02');
insert into Identty values('Project Wingman', '2020/12/01', 'Project Wingman_2020/12/01');
insert into Identty values('Phasmophobia', '2020/09/18', 'Phasmophobia_2020/09/18');
insert into Identty values('Dead by Daylight', '2016/12/01', 'Dead by Daylight_2016/12/01');
insert into Identty values('Among Us', '2018/11/16', 'Among Us_2018/11/16');
insert into Identty values('Satisfactory', '2020/06/08', 'Satisfactory_2020/06/08');
insert into Identty values('Fall Guys: Ultimate Knockout', '2020/08/04', 'Fall Guys: Ultimate Knockout_2020/08/04');
------------------
--GAME INSERTION--
------------------
--name, release, size, studio, mrp, link, image, desc, curver, defx2
insert into Game values ('Cyberpunk 2077', '2020/12/01', '70', 'CD PROJEKT RED', '2999', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://images.indianexpress.com/2020/11/cyberpunk2077.jpg', 'Cyberpunk 2077 is an open-world, action-adventure story set in Night City, a megalopolis obsessed with power, glamour and body modification. You play as V, a mercenary outlaw going after a one-of-a-kind implant that is the key to immortality.', '1.0.0', default, default);
insert into Game values('Red Dead Online', '2020/12/02', '150', 'Rockstar Games', '375', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/1404210/ss_11910cbe7b91268b17351baf2720af4f39395c08.1920x1080.jpg?t=1606871612', 'Step into the vibrant, ever-evolving world of Red Dead Online and experience life in frontier America. Chase down bounties, battle outlaw gangs and other players, hunt, fish and trade, search for exotic treasures, run Moonshine, and much more to discover in a world of astounding depth and detail.', '1.0.1', default, default);
insert into Game values('Project Wingman', '2020/12/01', '16', 'Sector D2', '569', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/895870/ss_a198aed40e8109bc44144a7aa693fc167d2b7487.1920x1080.jpg?t=1606868166', 'Project Wingman is a flight action game that lets you take the seat of advanced fighter jets and become a true ace. Fight in various missions and gamemodes ranging from intense aerial dogfights to large scale ground assault in an alternate scorched earth setting.', '1.0.2', default, default);
insert into Game values('Phasmophobia', '2020/09/18', '15', 'Kinetic Games', '439', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/739630/ss_59023d418d1825e574ad75911da34f5814a6bb9d.1920x1080.jpg?t=1606429609', 'Phasmophobia is a 4 player online co-op psychological horror. Paranormal activity is on the rise and it’s up to you and your team to use all the ghost hunting equipment at your disposal in order to gather as much evidence as you can.', '2.0.1', default, default);
insert into Game values('Dead by Daylight', '2016/12/01', '25', 'Behaviour Interactive Inc.', '569', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/1474030/ss_f31c9951bb396c3b1f4a3d177519b9472bb9e886.1920x1080.jpg?t=1606861292', 'Dead by Daylight is a multiplayer (4vs1) horror game where one player takes on the role of the savage Killer, and the other four players play as Survivors, trying to escape the Killer and avoid being caught and killed.', '12', default, default);
insert into Game values('Among Us', '2018/11/16', '0.25', 'Innersloth', '129', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/945360/ss_649e19ff657fa518d4c2b45bed7ffdc4264a4b3a.1920x1080.jpg?t=1606422465', 'An online and local party game of teamwork and betrayal for 4-10 players...in space!', '5', default, default);
insert into Game values('Satisfactory', '2020/06/08', '15', 'Coffee Stain Studios', '749', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/526870/ss_dcb79211f2f9bac1e6a2d85aad132fc3ae909001.1920x1080.jpg?t=1598908784', 'Satisfactory is a first-person open-world factory building game with a dash of exploration and combat. Play alone or with friends, explore an alien planet, create multi-story factories, and enter conveyor belt heaven!', '1.0.0', default, default);
insert into Game values('Fall Guys: Ultimate Knockout', '2020/08/04', '2', 'Mediatonic', '529', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/1097150/ss_a0758d69b45b016a386761e1415f2227542c27be.1920x1080.jpg?t=1606255678', 'Fall Guys is a massively multiplayer party game with up to 60 players online in a free-for-all struggle through round after round of escalating chaos until one victor remains!', '2.0', default, default);
----------------------
--CATEGORY INSERTION--
----------------------
--gid, catname
insert into Category values('Cyberpunk 2077_2020/12/01', 'FPS');
insert into Category values('Red Dead Online_2020/12/02', 'Open World');
insert into Category values('Project Wingman_2020/12/01', 'Simulation');
insert into Category values('Phasmophobia_2020/09/18', 'Horror');
insert into Category values('Dead by Daylight_2016/12/01', 'Horror');
insert into Category values('Among Us_2018/11/16', 'Casual');
insert into Category values('Satisfactory_2020/06/08', 'Simulation');
insert into Category values('Fall Guys: Ultimate Knockout_2020/08/04', 'Casual');
