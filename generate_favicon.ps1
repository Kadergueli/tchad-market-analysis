$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$outPath = Join-Path $PSScriptRoot 'favicon.ico'
$img = New-Object System.Drawing.Bitmap 64, 64
$g = [System.Drawing.Graphics]::FromImage($img)
$g.Clear([System.Drawing.Color]::FromArgb(15, 23, 42))
$pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(29, 78, 216), 2)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(15, 23, 42))
$g.FillRectangle($brush, 4, 4, 56, 56)
$g.DrawRectangle($pen, 4, 4, 55, 55)

$font = New-Object System.Drawing.Font('Arial', 28, [System.Drawing.FontStyle]::Bold)
$txt = 'FD'
$brushText = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255))
$size = $g.MeasureString($txt, $font)
$x = (64 - $size.Width) / 2
$y = (64 - $size.Height) / 2 - 2
$g.DrawString($txt, $font, $brushText, $x, $y)

$img.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Icon)
$g.Dispose()
$img.Dispose()
Write-Host "Created $outPath"
