<?php
  $nselect=$_GET["nselect"];
  if ($nselect == '') $nselect=6;

  $nload=$_GET["nload"];
  if ($nload == '') $nload=999;

  $datadate=$_GET["datadate"];
  if ($datadate == '') $datadate=date("Ymd");

  $prd=$_GET["prd"];
  if ($prd == '') $prd="mosaic";

  $legend=$_GET["legend"];
  if ($legend == '') 
    $legend=false;
  else
    $legend=true;

  $yyyy=substr($datadate,0,4);
  $mm=substr($datadate,4,2);
  $dd=substr($datadate,6,2);
       
  $data_dir='./data/'.$prd.'/'.$yyyy.'/'.$mm.'/'.$dd;
  $ImgArr = Array();

  if(!$legend){

  echo '<select id="radar_img_list" multiple="multiple" size="10">\n';


  $ImgDir=opendir($data_dir);
  while ($ImgFile = readdir($ImgDir)){
    if ($ImgFile!="." && $ImgFile!=".." && $ImgFile!="legend.png" && $ImgFile!="index.php") {
      $parts=explode(".",$ImgFile);
      $min=substr($parts[0],$parts[0].length-1,1);
      $ImgArr[count($ImgArr)] = $ImgFile;
    }
  }

  closedir($ImgDir);
  if (count($ImgArr) > 0) rsort($ImgArr);

  if (Count($ImgArr) < $nload ) $nload=Count($ImgArr);
  
  for($i=0; $i<$nload; $i++)
  {
    $parts=explode(".",$ImgArr[$i]);

    $isotimestamp=$parts[0];
    
    if ($i < $nselect ) {
      echo "<option selected='selected' value='".$isotimestamp.";".$data_dir."/".$ImgArr[$i]."'>";
    }else{
      echo "<option value='".$isotimestamp.";".$data_dir."/".$ImgArr[$i]."'>";
    }
    echo substr($isotimestamp,0,4)."-".substr($isotimestamp,4,2)."-".substr($isotimestamp,6,2)."  ";
    echo substr($isotimestamp,8,2).":".substr($isotimestamp,10,2)." UTC</option>\n";
  }
  echo '</select>';
  }else{
    echo '<img src="'.$data_dir.'/legend.png" />';
  }
?>

