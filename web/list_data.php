<select id="radar_img_list" multiple="multiple" size="10">
<?php
  $nselect=$_GET["nselect"];
  if ($nselect == '') $nselect=6;

  $nload=$_GET["nload"];
  if ($nload == '') $nload=999;

  $datadate=$_GET["datadate"];
  if ($datadate == '') $datadate=date("Ymd");

  $prd=$_GET["prd"];
  if ($prd == '') $prd="mosaic";

  $org=$_GET["org"];
  if ($org == '') $org="dmi";

  //$data_dir='./data/';
  //$data_dir='./data.dmi/mosaic/2010/08/02';
   if ($org =="smhi" && $prd == "mosaic") {
     $yyyy="2010";
     $mm="07";
     $dd="29";
   } else if ($org =="baltrad" && $prd == "ekxv") {
     $yyyy="2010";
     $mm="08";
     $dd="17";
   } else {
     //$yyyy="2010";
     //$mm="07";
     //$dd="29";
     $yyyy=substr($datadate,0,4);
     $mm=substr($datadate,4,2);
     $dd=substr($datadate,6,2);
   }

  $data_dir='./data.'.$org.'/'.$prd.'/'.$yyyy.'/'.$mm.'/'.$dd;
  //echo "<!-- data_dir='$data_dir' -->\n";
  echo "<!-- org='$org' -->\n";
  $ImgArr = Array();

  $ImgDir=opendir($data_dir);
  while ($ImgFile = readdir($ImgDir)){
    if ($ImgFile!="." && $ImgFile!=".." && $ImgFile!="index.php") {
      $parts=explode(".",$ImgFile);
      $min=substr($parts[0],$parts[0].length-1,1);
      if ($org =="dmi" && $prd == "mosaic" && $parts[4]==2000) {
        $ImgArr[count($ImgArr)] = $ImgFile;
      } else if ($org =="smhi" && $prd == "mosaic") {
        $ImgArr[count($ImgArr)] = $ImgFile;
      } else if ($prd == "ekrn" || $prd == "eksn" || $prd == "ekxr" || $prd == "ekxs" || $prd == "ekxv") {
        if ($parts[3]==500 && $min==0) {
       	  $min=substr($parts[0],$parts[0].length-1,1);
          $ImgArr[count($ImgArr)] = $ImgFile;
        }
      }
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
?>
</select>
