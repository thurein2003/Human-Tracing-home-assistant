Add-Type -AssemblyName System.Drawing
$src='EyeTrace_Final_Engineering\EyeTrace_Final_2_PLATES_R17_HORN_CLEANUP\RENDERS\CAD_BREP_MESH'
$out='EyeTrace_Final_Engineering\EyeTrace_Final_2_PLATES_R17_HORN_CLEANUP\RENDERS'
function Read-Stl($path){
 $b=[IO.File]::ReadAllBytes($path); $n=[BitConverter]::ToUInt32($b,80); $t=@()
 for($i=0;$i -lt $n;$i++){ $o=84+50*$i; $p=@(); for($j=0;$j -lt 3;$j++){ $v=@(); for($k=0;$k -lt 3;$k++){$v+=,[BitConverter]::ToSingle($b,$o+12+12*$j+4*$k)}; $p+=,@($v) }; $t+=,[PSCustomObject]@{P=$p} }
 return ,$t
}
function Draw-Stl($file,$png,$title,$plane){
 $tris=Read-Stl (Join-Path $src $file); $W=1600;$H=1100;$bmp=[Drawing.Bitmap]::new($W,$H);$g=[Drawing.Graphics]::FromImage($bmp);$g.SmoothingMode='AntiAlias';$g.Clear([Drawing.Color]::FromArgb(247,249,252))
 $data=@()
 foreach($tr in $tris){$p=$tr.P;$q=@();foreach($v in $p){ if($plane -eq 'XY'){$q+=,@([double]$v[0],[double]$v[1],[double]$v[2])} else {$q+=,@([double]$v[0],[double]$v[2],[double]$v[1])} };$data+=,[PSCustomObject]@{P=$q;D=(($q[0][2]+$q[1][2]+$q[2][2])/3)} }
 $all=@($data|ForEach-Object {$_.P}|ForEach-Object {$_});$xmin=($all|ForEach-Object {$_[0]}|Measure-Object -Minimum).Minimum;$xmax=($all|ForEach-Object {$_[0]}|Measure-Object -Maximum).Maximum;$ymin=($all|ForEach-Object {$_[1]}|Measure-Object -Minimum).Minimum;$ymax=($all|ForEach-Object {$_[1]}|Measure-Object -Maximum).Maximum
 $scale=[Math]::Min(($W-160)/($xmax-$xmin),($H-180)/($ymax-$ymin));$cx=$W/2;$cy=$H/2
 foreach($tr in ($data|Sort-Object D -Descending)){ $pts=@();foreach($v in $tr.P){$pts+=,[Drawing.PointF]::new([single]($cx+($v[0]-($xmin+$xmax)/2)*$scale),[single]($cy-($v[1]-($ymin+$ymax)/2)*$scale))};$avg=($tr.P|ForEach-Object {$_[2]}|Measure-Object -Average).Average;$shade=[Math]::Max(95,[Math]::Min(210,[int](165+($avg%17)*2)));$brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb($shade,116,65));$pen=[Drawing.Pen]::new([Drawing.Color]::FromArgb(55,35,22,30),0.35);$g.FillPolygon($brush,$pts);$g.DrawPolygon($pen,$pts);$brush.Dispose();$pen.Dispose() }
 $font=[Drawing.Font]::new('Arial',25,[Drawing.FontStyle]::Bold);$sub=[Drawing.Font]::new('Arial',17);$brush=[Drawing.SolidBrush]::new([Drawing.Color]::FromArgb(30,40,55));$g.DrawString($title,$font,$brush,50,35);$g.DrawString('FreeCAD 1.1.4 BREP tessellation • orthographic section/view • units mm',$sub,$brush,52,78);$g.DrawString(('Projected bounds: X {0:N1}..{1:N1} / {2} {3:N1}..{4:N1} mm' -f $xmin,$xmax,$plane,$ymin,$ymax),$sub,$brush,52,1050)
 $bmp.Save((Join-Path $out $png),[Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$bmp.Dispose()
}
Draw-Stl 'Pan_Full.stl' 'After_Pan_Interface_BREP_View.png' 'Pan carrier — R15 interface view' 'XY'
Draw-Stl 'Pan_Section.stl' 'After_Pan_Interface_BREP_Section.png' 'Pan carrier — center section' 'XZ'
Draw-Stl 'Tilt_Full.stl' 'After_Tilt_Interface_BREP_View.png' 'Tilt cradle — R15 interface view' 'XZ'
Draw-Stl 'Tilt_Section.stl' 'After_Tilt_Interface_BREP_Section.png' 'Tilt cradle — center section' 'XZ'

