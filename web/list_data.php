<?php
  $nselect=$_GET["nselect"];
  if ($nselect == '') $nselect=6;

  $nload=$_GET["nload"];
  if ($nload == '') $nload=999;

  $datadate=$_GET["datadate"];
  if ($datadate == '') $datadate=gmdate("YmdHi");

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
  $HH=substr($datadate,8,2);
  $MM=substr($datadate,10,2);

  date_default_timezone_set('UTC');
  $end_date = mktime($HH, $MM, 0, $mm, $dd, $yyyy);
  $start_date = strtotime("1 day ago", $end_date);

  $data_dir='./data/'.$prd.'/'.$yyyy.'/'.$mm.'/'.$dd;
  $data_dir_yesterday='./data/'.$prd.'/'.date('Y', $start_date).'/'.date('m', $start_date).'/'.date('d', $start_date);
  $ImgArr = Array();

  $legend_file = $data_dir.'/legend.png';

  if(file_exists($legend_file)){
    echo '<img src="'.$legend_file.'" />';
  } else {
    echo '<img src="./img/scl.png">';
  }

  echo "\n";

  echo '<select id="radar_img_list" multiple="multiple" size="10">';
  echo "\n";


  $ImgDir=opendir($data_dir_yesterday);
  while ($ImgFile = readdir($ImgDir)){
    if ($ImgFile!="." && $ImgFile!=".." && $ImgFile!="legend.png" && $ImgFile!="index.php") {
      $parts=explode(".",$ImgFile);
      $min=substr($parts[0],$parts[0].length-1,1);
      $ImgArr[count($ImgArr)] = $ImgFile;
    }
  }
  closedir($ImgDir);

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

  $cnt = 0;
  
  for($i=0; $i<$nload; $i++)
  {
    $parts=explode(".",$ImgArr[$i]);

    $isotimestamp=$parts[0];
    $yyyy=substr($isotimestamp,0,4);
    $mm=substr($isotimestamp,4,2);
    $dd=substr($isotimestamp,6,2);
    $HH=substr($isotimestamp,8,2);
    $MM=substr($isotimestamp,10,2);
    $data_dir='./data/'.$prd.'/'.$yyyy.'/'.$mm.'/'.$dd;
    date_default_timezone_set('UTC');
    $current_date = mktime($HH, $MM, 0, $mm, $dd, $yyyy);
    
    if ($current_date < $start_date || $current_date > $end_date)
      continue;

    if ($cnt < $nselect ) {
      echo "<option selected='selected' value='".$isotimestamp.";".$data_dir."/".$ImgArr[$i]."'>";
    }else{
      echo "<option value='".$isotimestamp.";".$data_dir."/".$ImgArr[$i]."'>";
    }
    $cnt++;
    echo substr($isotimestamp,0,4)."-".substr($isotimestamp,4,2)."-".substr($isotimestamp,6,2)."  ";
    echo substr($isotimestamp,8,2).":".substr($isotimestamp,10,2)." UTC</option>\n";
  }
  echo '</select>';
?>

