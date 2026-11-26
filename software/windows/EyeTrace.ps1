[CmdletBinding()]
param(
    [ValidateSet('Check','Install','Model','Pi','Tunnel','Text','Vision','Dashboard')]
    [string]$Action = 'Check',
    [string]$SshTarget = $env:EYETRACE_SSH_TARGET,
    [string]$ImagePath,
    [switch]$ApproveInstall
)
$ErrorActionPreference = 'Stop'

function Get-ConfiguredPort([string]$Value, [int]$Default) {
    if ([string]::IsNullOrEmpty($Value)) { return $Default }
    $port = 0
    if (-not [int]::TryParse($Value, [ref]$port) -or $port -lt 1 -or $port -gt 65535) {
        throw "Invalid TCP port: $Value"
    }
    return $port
}

function Invoke-EyeTraceSsh([string[]]$SshOptions, [string[]]$RemoteCommand = @()) {
    if ($SshTarget -notmatch '^(?:[A-Za-z_][A-Za-z0-9_.-]*@)?(?:[A-Za-z0-9][A-Za-z0-9.-]*|\[[0-9A-Fa-f:]+\])$') {
        throw 'Set EYETRACE_SSH_TARGET to your SSH user and hostname or IP.'
    }
    & ssh.exe @SshOptions $SshTarget @RemoteCommand
    if ($LASTEXITCODE -ne 0) { throw "SSH exited with code $LASTEXITCODE" }
}

function Get-LocalOllama {
    Invoke-RestMethod -Uri "$ollama/api/tags" -TimeoutSec 5
}

$aiLocal = Get-ConfiguredPort $env:EYETRACE_WINDOWS_OLLAMA_PORT 11434
$aiRemote = Get-ConfiguredPort $env:EYETRACE_PI_OLLAMA_PORT 11435
$webLocal = Get-ConfiguredPort $env:EYETRACE_WINDOWS_WEB_PORT 8081
$webRemote = Get-ConfiguredPort $env:EYETRACE_PI_WEB_PORT 8080
$ollama = "http://127.0.0.1:$aiLocal"
$model = $env:EYETRACE_MODEL
if (-not $model) { $model = 'gemma3:4b' }
if ($model -notmatch '^[A-Za-z0-9][A-Za-z0-9._:/-]*$' -or $model -match ':cloud$') {
    throw 'Choose a local Ollama model name.'
}

switch ($Action) {
    'Check' {
        Get-Command ollama.exe -ErrorAction Stop | Select-Object Name, Source
        Get-LocalOllama
    }
    'Install' {
        if (Get-Command ollama.exe -ErrorAction SilentlyContinue) { return }
        if (-not $ApproveInstall) { throw 'Review https://ollama.com/download/windows and pass -ApproveInstall to open the vendor download.' }
        Start-Process 'https://ollama.com/download/windows'
    }
    'Model' {
        if ($model -notin (Get-LocalOllama).models.name) {
            $oldHost = $env:OLLAMA_HOST
            try {
                $env:OLLAMA_HOST = "127.0.0.1:$aiLocal"
                & ollama.exe pull $model
                if ($LASTEXITCODE -ne 0) { throw "Ollama pull exited with code $LASTEXITCODE" }
            } finally {
                $env:OLLAMA_HOST = $oldHost
            }
            if ($model -notin (Get-LocalOllama).models.name) { throw "Model missing after pull: $model" }
        }
    }
    'Pi' {
        Invoke-EyeTraceSsh -SshOptions @('-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes') -RemoteCommand @('true')
    }
    'Tunnel' {
        Get-LocalOllama | Out-Null
        Invoke-EyeTraceSsh -SshOptions @('-N','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=yes','-o','ExitOnForwardFailure=yes',
            '-o','ServerAliveInterval=30','-o','ServerAliveCountMax=3',
            '-R',"127.0.0.1:${aiRemote}:127.0.0.1:${aiLocal}",
            '-L',"127.0.0.1:${webLocal}:127.0.0.1:${webRemote}")
    }
    { $_ -in 'Text','Vision' } {
        if ($model -notin (Get-LocalOllama).models.name) { throw "Local model missing: $model" }
        $body = @{ model = $model; stream = $false; prompt = 'Reply with exactly EYETRACE_OK.' }
        if ($Action -eq 'Vision') {
            if (-not $ImagePath) { throw 'Pass -ImagePath with a local JPEG or PNG.' }
            $image = Get-Item -LiteralPath $ImagePath -ErrorAction Stop
            if ($image.PSIsContainer -or $image.Extension -notin '.jpg','.jpeg','.png' -or $image.Length -gt 10000000) {
                throw 'Choose a JPEG or PNG file up to 10 MB.'
            }
            $body.prompt = 'Describe the visible objects and their positions in this image.'
            $body.images = @([Convert]::ToBase64String([IO.File]::ReadAllBytes($image.FullName)))
        }
        $parameters = @{ Method = 'Post'; Uri = "$ollama/api/generate"; ContentType = 'application/json'
                         Body = ($body | ConvertTo-Json -Compress); TimeoutSec = 180 }
        Invoke-RestMethod @parameters
    }
    'Dashboard' { Start-Process "http://127.0.0.1:$webLocal" }
}
