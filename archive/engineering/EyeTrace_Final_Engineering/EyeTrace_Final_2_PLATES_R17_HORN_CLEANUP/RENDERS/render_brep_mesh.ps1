Add-Type -AssemblyName System.Drawing
$src='EyeTrace_Final_Engineering\EyeTrace_Final_2_PLATES_R17_HORN_CLEANUP\RENDERS\CAD_BREP_MESH'
$out='EyeTrace_Final_Engineering\EyeTrace_Final_2_PLATES_R17_HORN_CLEANUP\RENDERS'
function Draw-Stl($file,$png,$title,$plane,$window){
 $b=[IO.File]::ReadAllBytes((Join-Path $src $file));$n=[BitConverter]::ToUInt32($b,80);$tris=[System.Collections.Generic.List[object]]::new();$xs=[System.Collections.Generic.List[double]]::new();$ys=[System.Collections.Generic.List[double]]::new()
 for($i=0;$i -lt $n;$i++){ $o=84+50*$i;$P=@();for($j=0;$j -lt 3;$j++){ $x=[double][BitConverter]::ToSingle($b,$o+12+12*$j);$y=[double][BitConverter]::ToSingle($b,$o+16+12*$j);$z=[double][BitConverter]::ToSingle($b,$o+20+12*$j);switch($plane){'XY'{$u=$x;$v=$y;$dep=$z};'XZ'{$u=$x;$v=$z;$dep=$y};'YZ'{$u=$y;$v=$z;$dep=$x}};$P+=,[PSCustomObject]@{U=$u;V=$v;D=$dep};$xs.Add($u);$ys.Add($v)};$cu=($P[0].U+$P[1].U+$P[2].U)/3;$cv=($P[0].V+$P[1].V+$P[2].V)/3;if($cu -ge $window[0] -and $cu -le $window[1] -and $cv -ge $window[2] -and $cv -le $window[3]){$tris.Add([PSCustomObject]@{P=$P;D=($P[0].D+$P[1].D+$P[2].D)/3})} }
 if($tris.Count -eq 0){throw "No triangles selected $file"}
 $xmin=($tris|ForEach-Object {$_.P}|ForEach-Object {$_.U}|Measure-Object -Minimum).Minimum;$xmax=($tris|ForEach-Object {$_.P}|ForEach-Object {$_.U}|Measure-Object -Maximum).Maximum;$ymin=($tris|ForEach-Object {$_.P}|ForEach-Object {$_.V}|Measure-Object -Minimum).Minimum;$ymax=($tris|ForEach-Object {$_.P}|ForEach-Object {$_.V}|Measure-Object -Maximum).Maximum
 $W=1600;$H=1100;$scale=[Math]::Min(($W-180)/($xmax-$xmin),($H-220)/($ymax-$ymin));$cx=$W/2;$cy=$H/2;$bmp=[Drawing.Bitmap]::new($W,$H);$g=[Drawing.Graphics]::FromImage($bmp);$g.SmoothingMode='AntiAlias';$g.Clear([Drawing.Color]::FromArgb(250,251,253))
 foreach($tr in ($tris|Sort-Object D -Descending)){ $pts=[Drawing.PointF[]]@();foreach($q in $tr.P){$pts+=,[Drawing.PointF]::new([single]($cx+($q.U-($xmin+$xmax)/2)*$scale),[single]($cy-($q.V-($ymin+$ymax)/2)*$scale))};$brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(132,173,214));$g.FillPolygon($brush,$pts);$brush.Dispose()}
 $font=[Drawing.Font]::new('Arial',25,[Drawing.FontStyle]::Bold);$sub=[Drawing.Font]::new('Arial',17);$brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(25,35,48));$g.DrawString($title,$font,$brush,50,35);$g.DrawString('FreeCAD 1.1.4 BREP-derived mesh view • section plane shown • mm',$sub,$brush,52,78);$g.DrawString(('Visible extent: {0:N1} × {1:N1} mm' -f ($xmax-$xmin),($ymax-$ymin)),$sub,$brush,52,1050);$bmp.Save((Join-Path $out $png),[Drawing.Imaging.ImageFormat]::Png);$brush.Dispose();$font.Dispose();$sub.Dispose();$g.Dispose();$bmp.Dispose()
}
Draw-Stl 'Pan_Full.stl' 'After_Pan_Interface_BREP_View.png' 'Pan horn seat — underside detail' 'XY' @(-25,25,-25,25)
Draw-Stl 'Pan_Section.stl' 'After_Pan_Interface_BREP_Section.png' 'Pan horn seat — vertical section' 'XZ' @(-25,25,31,40)
Draw-Stl 'Tilt_Full.stl' 'After_Tilt_Interface_BREP_View.png' 'Tilt horn seat — output-face detail' 'YZ' @(-25,25,53,102)
Draw-Stl 'Tilt_Section.stl' 'After_Tilt_Interface_BREP_Section.png' 'Tilt horn seat — vertical section' 'XZ' @(-44,-32,55,101)

