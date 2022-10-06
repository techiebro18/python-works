CKEditor Plugin Uploader
=============
ckeditor plugin for fast upload image to editor.
Install
------------
Create folder `ckeditor/plugins/uploader` and unpack archive to 

File `ckeditor/config.js`

	CKEDITOR.editorConfig = function( config ){
		config.extraPlugins = 'uploader'; // add plugin
		config.uploadFolder = 'http://xdan/images/'; // report plugin which will fill
	};
	
File `ckeditor/plugins/uploader/uploader.php`

	$config = array(
		'access_types' =>array('jpeg', 'jpg', 'png', 'bmp', 'gif',), // allowed extensions file
		'folder' => $_SERVER['DOCUMENT_ROOT'].'/images/',// full path
		'use_md5'=>true, // change the name on the md5 hash
		'replace'=>false, // replace the file with the same name, only works with use_md5
	);

1. [Demo][demo]
2. [Author][author]
3. [more ckeditor Plugins][more]
[demo]: http://xdan.ru/project/ckplugins/#demo_uploader
[author]: http://xdan.ru/user/profile/Leroy
[more]: http://xdan.ru/project/ckplugins/