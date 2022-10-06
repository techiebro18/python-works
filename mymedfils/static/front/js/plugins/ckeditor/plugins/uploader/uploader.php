<?php
$config = array(
	// 'access_types' =>array('jpeg', 'jpg', 'png', 'bmp', 'gif', 'cdr', 'swf',  'psd', 'zip', 'rar', '7z', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'html','avi','cs','exe','fla','mp3','pdf','ppt'),
	'access_types' =>array('jpeg', 'jpg', 'png', 'bmp', 'gif'),
    'folder' => $_SERVER['DOCUMENT_ROOT'].'/public/uploads/images/',// меняем путь до фото
    //'folder' => $_SERVER['DOCUMENT_ROOT'].'/ask/public/uploads/images/',// меняем путь до фото
	//'folder' => $_SERVER['DOCUMENT_ROOT'].'/public/uploads/images/',// меняем путь до фото
	'use_md5'=>true, // менять имя на md5 хеш
	'replace'=>false, // заменять файл с тем же именем, работает только с вместе с use_md5
);
function resize_image($file, $name,$w=900, $h=400, $crop=FALSE) {
	global $config;
    list($width, $height) = getimagesize($file);
    $r = $width / $height;
    $w = 900;
    if ($crop) {
        if ($width > $height) {
            $width = ceil($width-($width*abs($r-$w/$h)));
        } else {
            $height = ceil($height-($height*abs($r-$w/$h)));
        }
        $newwidth = $w;
        $newheight = $h;
    } else {
        // if ($w/$h > $r) {
        //     $newwidth = $h*$r;
        //     $newheight = $h;
        // } else {
        //     $newheight = $w/$r;
        //     $newwidth = $w;
        // }

        if($w<$width){
            $newheight = $w/$r;
            $newwidth = $w;            
        }
        else{
            $newwidth = $width;
            $newheight = $height;
        }

    }
    $src = imagecreatefromjpeg($file);
    $dst = imagecreatetruecolor($newwidth, $newheight);
    imagecopyresampled($dst, $src, 0, 0, 0, 0, $newwidth, $newheight, $width, $height);
    $donemoving = imagejpeg ( $dst , $config['folder'].$name );
    var_dump($donemoving);
    die();
    return $dst;
}

function resize($newWidth, $targetFile, $originalFile) {

    $info = getimagesize($originalFile);
    $mime = $info['mime'];

    switch ($mime) {
            case 'image/jpeg':
                    $image_create_func = 'imagecreatefromjpeg';
                    $image_save_func = 'imagejpeg';
                    $new_image_ext = 'jpg';
                    break;

            case 'image/png':
                    $image_create_func = 'imagecreatefrompng';
                    $image_save_func = 'imagepng';
                    $new_image_ext = 'png';
                    break;

            case 'image/gif':
                    $image_create_func = 'imagecreatefromgif';
                    $image_save_func = 'imagegif';
                    $new_image_ext = 'gif';
                    break;

            default: 
                    throw new Exception('Unknown image type.');
    }

    $img = $image_create_func($originalFile);
    list($width, $height) = getimagesize($originalFile);
    if($newWidth < $width){
        $newHeight = ($height / $width) * $newWidth;        
    }
    else{
        $newHeight = $height;
        $newWidth = $width;
    }

    $tmp = imagecreatetruecolor($newWidth, $newHeight);
    imagecopyresampled($tmp, $img, 0, 0, 0, 0, $newWidth, $newHeight, $width, $height);
    if (file_exists($targetFile)) {
            unlink($targetFile);
    }
    return $image_save_func($tmp, "$targetFile.$new_image_ext");
}



function getk($val,$k=0){
	return is_array($val)?$val[$k]:$val;
}


// function saveFile( $k=0,$fileElementName = 'image' ){
//     global $config;
//     if( !getk($_FILES[$fileElementName]['error'],$k) and getk($_FILES[$fileElementName]['tmp_name'],$k) and getk($_FILES[$fileElementName]['tmp_name'],$k) != 'none' ){
//         $name = getk($_FILES[$fileElementName]['name'],$k);
//         $typ = pathinfo($name, PATHINFO_EXTENSION);
//         $targetName = rtrim($name,".".$typ);
//         $targetFileName = $targetName . "." . $typ;
//         $typ = strtolower($typ);
//         if( in_array($typ,$config['access_types']) ){
//             $uploaded = resize(800, $config['folder'].$targetName, getk($_FILES[$fileElementName]['tmp_name'],$k));
//             if($uploaded){
//                 $fi = pathinfo($config['folder'].$name);
//                 $obj = isset($fi["extension"])?strtolower($fi["extension"]):'';
//                 if( in_array($obj,$config['access_types']) ){
//                     $k1 = '';
//                     if( $config['use_md5'] ){
//                         if( !$config['replace'] )
//                             while( file_exists($config['folder'].md5($name.$k1).'.'.$obj) )$k1.='1';
//                         rename($config['folder'].$name,$config['folder'].md5($name.$k1).'.'.$obj);
//                         return $name.'='.md5($name.$k1).'.'.$obj;
//                     }else return $name.'='.$name.'.'.$obj;
//                 }else unlink($config['folder'].$name);
//             }
//         }   
//     }
// }

function saveFile( $k=0,$fileElementName = 'image' ){
	global $config;
	if( !getk($_FILES[$fileElementName]['error'],$k) and getk($_FILES[$fileElementName]['tmp_name'],$k) and getk($_FILES[$fileElementName]['tmp_name'],$k) != 'none' ){
		$name = getk($_FILES[$fileElementName]['name'],$k);
		$typ = pathinfo($name, PATHINFO_EXTENSION);
		$targetName = rtrim($name,".".$typ);
        $typ = strtolower($typ);
        if($typ == "jpg" || $typ == "jpeg"){
            $typ = "jpg";
        }
        $targetFileName = $targetName . "." . $typ;
		if( in_array($typ,$config['access_types']) ){
			$uploaded = resize(800, $config['folder'].$targetName, getk($_FILES[$fileElementName]['tmp_name'],$k));
			if($uploaded){
				$fi = pathinfo($config['folder'].$targetFileName);
				$obj = isset($fi["extension"])?strtolower($fi["extension"]):'';
				if( in_array($obj,$config['access_types']) ){
					$k1 = '';
					if( $config['use_md5'] ){
						if( !$config['replace'] )
							while( file_exists($config['folder'].md5($targetFileName.$k1).'.'.$obj) )$k1.='1';
						rename($config['folder'].$targetFileName,$config['folder'].md5($targetFileName.$k1).'.'.$obj);
						return $targetFileName.'='.md5($targetFileName.$k1).'.'.$obj;
					}else return $targetFileName.'='.$targetFileName.'.'.$obj;
				}else unlink($config['folder'].$targetFileName);
			}
		}	
	}
}

if( isset($_FILES['image']['name'])and is_array($_FILES['image']['name']) ){
	$val = array();
	foreach($_FILES['image']['name'] as $k=>$name){
		$val[]=saveFile($k);
	}
	die(implode(';',$val));
};
?>
