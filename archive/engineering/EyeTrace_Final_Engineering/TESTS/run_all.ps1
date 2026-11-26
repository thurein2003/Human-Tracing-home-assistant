param([string]$FreeCADPython = 'D:\App files\bin\python.exe')
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$taskRun = 'recheck_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
& $FreeCADPython "$PSScriptRoot\validate_geometry_assembly_motion.py" $taskRun
if ($LASTEXITCODE -ne 0) { throw 'Assembly/motion script failed' }
$taskSummary = Get-Content -LiteralPath "$PSScriptRoot\results\$taskRun\checks\independent_validation_summary.json" -Raw | ConvertFrom-Json
if ($taskSummary.critical_software_failures.Count -gt 0 -or $taskSummary.motion_penetrations -gt 0) { throw 'Assembly/motion validation failed' }
foreach ($taskScript in @('validate_contacts_access.py','validate_camera_tool_access.py','measure_servo_geometry.py','validate_wall_sections.py','assess_loads.py','export_and_validate.py','delivery_QA.py')) {
    & $FreeCADPython "$PSScriptRoot\$taskScript"
    if ($LASTEXITCODE -ne 0) { throw "Failed: $taskScript" }
}
Write-Output 'Nominal CAD/export QA passed. Review new timestamped motion output, refresh documents/rendering/archive after edits; physical fit remains unverified.'
