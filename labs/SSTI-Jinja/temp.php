<?php
    if(isset($_POST["username"]) && isset($_POST["pwd"])){
        $yuf85e0677=$_POST["username"];
        $rs35c246d5=$_POST["pwd"];
        if($yuf85e0677==$rs35c246d5){
            echo base64_decode("\x50\x47\112\x79\x4c\172\x35\x47\x59\127\154\163\132\127\x51\x68\111\x45\x35\166\x49\x47\132\163\131\127\x63\x67\x5a\155\71\171\111\x48\x6c\166\x64\x51\x3d\x3d");}
        else {
            if(sha1($yuf85e0677)===sha1($rs35c246d5)){
                echo file_get_contents(base64_decode("\x4c\151\64\166\x5a\x6d\x78\x68\x5a\x79\65\60\145\110\x51\75"));
            } else {
                echo base64_decode("\x50\107\112\171\x4c\x7a\65\107\x59\x57\154\x73\x5a\127\x51\x68\x49\105\x35\x76\111\x47\132\x73\131\127\x63\x67\x5a\155\71\x79\x49\110\154\x76\x64\x51\x3d\75");
            }
        }
    }
?>