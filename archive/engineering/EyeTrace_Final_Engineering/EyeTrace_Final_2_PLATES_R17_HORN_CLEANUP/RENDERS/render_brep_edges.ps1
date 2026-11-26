Add-Type -AssemblyName System.Drawing
$root='EyeTrace_Final_Engineering\EyeTrace_Final_2_PLATES_R17_HORN_CLEANUP'
$j=Get-Content -LiteralPath (Join-Path $root 'RENDERS\BREP_LINE_DATA.json') -Raw|ConvertFrom-Json
function Render-Edges($key,$field,$file,$title,$xmin,$xmax,$ymin,$ymax,$caption){
 $xmin=[double]$xmin;$xmax=[double]$xmax;$ymin=[double]$ymin;$ymax=[double]$ymax;$paths=$j.$key.$field;$W=1600;$H=1100;$bmp=[Drawing.Bitmap]::new($W,$H);$g=[Drawing.Graphics]::FromImage($bmp);$g.SmoothingMode='AntiAlias';$g.Clear([Drawing.Color]::FromArgb(250,251,253))
 $scale=[Math]::Min(($W-220)/($xmax-$xmin),($H-260)/($ymax-$ymin));$cx=$W/2;$cy=$H/2
 $pen=[Drawing.Pen]::new([Drawing.Color]::FromArgb(35,70,110),2.2);$pen.LineJoin='Round'
 foreach($path in $paths){if($path.Count -lt 2){continue};$pts=[Drawing.PointF[]]@();foreach($q in $path){$px=$cx+([double]$q[0]-($xmin+$xmax)/2)*$scale;$py=$cy-([double]$q[1]-($ymin+$ymax)/2)*$scale;$pts+=,[Drawing.PointF]::new([single]$px,[single]$py)};if($pts.Count -gt 1){$g.DrawLines($pen,$pts)}}
 $font=[Drawing.Font]::new('Arial',26,[Drawing.FontStyle]::Bold);$sub=[Drawing.Font]::new('Arial',18);$brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(25,35,48));$g.DrawString($title,$font,$brush,45,32);$g.DrawString('FreeCAD 1.1.4 BREP edges • orthographic mm view',$sub,$brush,47,78);$g.DrawString($caption,$sub,$brush,47,1045);$bmp.Save((Join-Path $root ('RENDERS\'+$file)),[Drawing.Imaging.ImageFormat]::Png);$pen.Dispose();$brush.Dispose();$font.Dispose();$sub.Dispose();$g.Dispose();$bmp.Dispose()
}
Render-Edges 'Pan' 'seat' 'After_Pan_Interface_BREP_View.png' 'Pan horn seat — underside R15 profile' '-38' '38' '-38' '38' 'View bounds: X/Y ±38 mm'
Render-Edges 'Tilt' 'seat' 'After_Tilt_Interface_BREP_View.png' 'Tilt horn seat — output-face R15 profile' '-23' '23' '54' '102' 'View bounds: transverse ±23 mm, vertical 54–102 mm'
Render-Edges 'Pan' 'section' 'After_Pan_Interface_BREP_Section.png' 'Pan horn seat — section through output axis' '-25' '25' '31' '42' 'Section plane X=0 mm; local pocket floor follows R15 depth 1.7 mm'
Render-Edges 'Tilt' 'section' 'After_Tilt_Interface_BREP_Section.png' 'Tilt horn seat — section through output axis' '-43' '-31' '55' '101' 'Section plane Y=0 mm; local pocket floor follows R15 depth 1.7 mm'





