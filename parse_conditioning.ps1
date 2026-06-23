# PowerShell script to parse FORGE conditioning library and classify protocols

$content = Get-Content -Path D:\forge\FORGE_CONDITIONING_LIBRARY_V1.md -Raw

# Split by protocol headers
$protocolSections = $content -split '(?=#### [A-Z]{2}-[0-9]{3}:)'
$protocolSections = $protocolSections[1..($protocolSections.Length-1)] # Remove first empty element

$protocols = @()

foreach ($section in $protocolSections) {
    if ($section -match '#### ([A-Z]{2}-[0-9]{3}):?\s*(.*)') {
        $code = $matches[1]
        $name = $matches[2].Trim()
        
        # Extract fields
        $system = ""
        $level = ""
        $environment = ""
        $fatigueScore = ""
        
        if ($section -match '\*\*System\*\*\s*\|\s*([^|]+)') {
            $system = $matches[1].Trim()
        }
        
        if ($section -match '\*\*Level\*\*\s*\|\s*([^|]+)') {
            $level = $matches[1].Trim()
        }
        
        if ($section -match '\*\*Environment\*\*\s*\|\s*([^|]+)') {
            $environment = $matches[1].Trim()
        }
        
        if ($section -match '\*\*Fatigue Score\*\*\s*\|\s*([^|]+)') {
            $fatigueScore = $matches[1].Trim()
        }
        
        # Determine category based on environment
        $category = ""
        if ($environment -match '(?i)gym|pool|bike|treadmill|stationary') {
            $category = "GYM_CONDITIONING"
        } elseif ($environment -match '(?i)court|badminton|tennis') {
            $category = "COURT_CONDITIONING"
        } elseif ($environment -match '(?i)field|track|road|trail|turf|grass|hill|measured') {
            $category = "FIELD_CONDITIONING"
        } elseif ($system -match 'Recovery Conditioning') {
            $category = "RECOVERY_CONDITIONING"
        } else {
            # Default to field if not clearly categorized
            $category = "FIELD_CONDITIONING"
        }
        
        $protocols += [pscustomobject]@{
            Code = $code
            Name = $name
            System = $system
            Level = $level
            Environment = $environment
            FatigueScore = $fatigueScore
            Category = $category
        }
    }
}

# Output summary
Write-Host "Total protocols found: $($protocols.Count)`n"

# Group by category
$categories = $protocols | Group-Object -Property Category

foreach ($category in $categories) {
    Write-Host "=== $($category.Name) ==="
    Write-Host "Count: $($category.Count)"
    
    # Level distribution
    $levels = $category.Group | Group-Object -Property Level
    Write-Host "Level distribution:"
    foreach ($level in $levels) {
        Write-Host "  $($level.Name): $($level.Count)"
    }
    
    # Energy system distribution
    $systems = $category.Group | Group-Object -Property System
    Write-Host "Energy system distribution:"
    foreach ($system in $systems) {
        Write-Host "  $($system.Name): $($system.Count)"
    }
    
    Write-Host ""
}

# Detailed breakdown for each category
Write-Host "=== DETAILED CATEGORY BREAKDOWN ==="
foreach ($categoryName in $categories.Name) {
    Write-Host "`n=== $categoryName ==="
    $categoryProtocols = $protocols | Where-Object {$_.Category -eq $categoryName}
    
    # Protocol list
    Write-Host "Protocols:"
    foreach ($protocol in $categoryProtocols) {
        Write-Host "  $($protocol.Code): $($protocol.Name) [$($protocol.System)]"
    }
    
    # Missing protocol types analysis
    Write-Host ""
    Write-Host "Analysis:"
    
    # Check for missing environment types in this category
    switch ($categoryName) {
        "FIELD_CONDITIONING" {
            $hasTrack = $categoryProtocols.Environment -match '(?i)track'
            $hasField = $categoryProtocols.Environment -match '(?i)field'
            $hasRoad = $categoryProtocols.Environment -match '(?i)road'
            $hasTrail = $categoryProtocols.Environment -match '(?i)trail'
            $hasTurf = $categoryProtocols.Environment -match '(?i)turf'
            $hasGrass = $categoryProtocols.Environment -match '(?i)grass'
            $hasHill = $categoryProtocols.Environment -match '(?i)hill'
            
            Write-Host "  Track-based: $($hasTrack)"
            Write-Host "  Field-based: $($hasField)"
            Write-Host "  Road-based: $($hasRoad)"
            Write-Host "  Trail-based: $($hasTrail)"
            Write-Host "  Turf-based: $($hasTurf)"
            Write-Host "  Grass-based: $($hasGrass)"
            Write-Host "  Hill-based: $($hasHill)"
        }
        "COURT_CONDITIONING" {
            $hasBadminton = $categoryProtocols.Environment -match '(?i)badminton'
            $hasTennis = $categoryProtocols.Environment -match '(?i)tennis'
            $hasCourt = $categoryProtocols.Environment -match '(?i)court'
            
            Write-Host "  Badminton-specific: $($hasBadminton)"
            Write-Host "  Tennis-specific: $($hasTennis)"
            Write-Host "  General court: $($hasCourt)"
        }
        "GYM_CONDITIONING" {
            $hasGym = $categoryProtocols.Environment -match '(?i)gym'
            $hasPool = $categoryProtocols.Environment -match '(?i)pool'
            $hasBike = $categoryProtocols.Environment -match '(?i)bike'
            $hasTreadmill = $categoryProtocols.Environment -match '(?i)treadmill'
            $hasStationary = $categoryProtocols.Environment -match '(?i)stationary'
            
            Write-Host "  Gym-based: $($hasGym)"
            Write-Host "  Pool-based: $($hasPool)"
            Write-Host "  Bike-based: $($hasBike)"
            Write-Host "  Treadmill-based: $($hasTreadmill)"
            Write-Host "  Stationary equipment: $($hasStationary)"
        }
        "RECOVERY_CONDITIONING" {
            $hasActive = $categoryProtocols.System -match '(?i)active'
            $hasMobility = $categoryProtocols.System -match '(?i)mobility'
            $hasAqua = $categoryProtocols.Environment -match '(?i)pool|aqua'
            $hasCycling = $categoryProtocols.Environment -match '(?i)bike|cycling'
            
            Write-Host "  Active recovery: $($hasActive)"
            Write-Host "  Mobility focus: $($hasMobility)"
            Write-Host "  Aquatic: $($hasAqua)"
            Write-Host "  Cycling-based: $($hasCycling)"
        }
    }
    
    Write-Host ""
}