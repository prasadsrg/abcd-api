insert into access_data(code, name, val) values ('MENU', 'Dashboard'	, 'DASHBOARD'	);
insert into access_data(code, name, val) values ('MENU', 'App Data'	, 'APP_DATA'	);
insert into access_data(code, name, val) values ('MENU', 'Consumer'	, 'CONSUMER'	);
insert into access_data(code, name, val) values ('MENU', 'Branches'	, 'BRANCHES'	);
insert into access_data(code, name, val) values ('MENU', 'Profiles'	, 'PROFILES'	);
insert into access_data(code, name, val) values ('MENU', 'Reports'	, 'REPORTS'		);
insert into access_data(code, name, val) values ('MENU', 'Settings'	, 'SETTINGS'	);
insert into access_data(code, name, val) values ('MENU', 'Access Menu', 'ACCESS_MENU'	);

insert into access_data (val, name, code, data)  values('CONSUMER', 'Consumers Report', 'REPORT', '/consumer');

insert into access_data(val, name,  code) values('CONSUMER_CONSUMER', 'consumer',  'REPORT_CONSUMER');
insert into access_data(val, name,  code) values('CONSUMER_FROMDATE', 'fromDate', 'REPORT_CONSUMER');
insert into access_data(val, name, code) values('CONSUMER_TODATE', 'toDate', 'REPORT_CONSUMER');


insert into vendor(id, title, name) values('DFF', 'DFFTech', 'DFF Tech');
insert into address(id) values('DFF_MAIN_BRANCH');
INSERT INTO branch (id, name, vid, is_main, address_id ) VALUES ('DFF_MAIN_BRANCH','DL Tech', 'DFF', true, 'DFF_MAIN_BRANCH');

insert into img( id)  values('SUPPORT_DFF_IMG');
insert into address(id) values('SUPPORT_DFF_ADDRESS');

INSERT INTO profile (id, name, email, mobile, password, role, branch_id, img_id, address_id, vid)
    VALUES ('SUPPORT_DFF_USER','Support User','support@dfftech.com','123456789', '1234', 'SUPER_ADMIN',  'DFF_MAIN_BRANCH', 'SUPPORT_DFF_IMG', 'SUPPORT_DFF_ADDRESS', 'DFF');


