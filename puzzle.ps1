# Interactive Linear Equation Puzzle Game

function Generate-LinearSystem {
    # Generate random 2-digit solutions for x and y
    $x = Get-Random -Minimum 10 -Maximum 20
    $y = Get-Random -Minimum 10 -Maximum 20
    
    # Generate coefficients (1-9, ensure system is solvable)
    do {
        $a1 = Get-Random -Minimum 1 -Maximum 10
        $b1 = Get-Random -Minimum 1 -Maximum 10
        $a2 = Get-Random -Minimum 1 -Maximum 10
        $b2 = Get-Random -Minimum 1 -Maximum 10
    } while (($a1 * $b2 - $a2 * $b1) -eq 0)
    
    # Calculate constants
    $c1 = $a1 * $x + $b1 * $y
    $c2 = $a2 * $x + $b2 * $y
    
    # Format equations
    $eq1 = Format-Equation -a $a1 -b $b1 -c $c1
    $eq2 = Format-Equation -a $a2 -b $b2 -c $c2
    
    return @{
        Equation1 = $eq1
        Equation2 = $eq2
        Solution = @{x = $x; y = $y}
    }
}

function Format-Equation {
    param($a, $b, $c)
    
    $equation = ""
    
    # First term
    if ($a -eq 1) {
        $equation += "x"
    } else {
        $equation += "$a" + "x"
    }
    
    # Second term
    if ($b -ge 0) {
        if ($b -eq 1) {
            $equation += " + y"
        } else {
            $equation += " + $b" + "y"
        }
    } else {
        if ($b -eq -1) {
            $equation += " - y"
        } else {
            $equation += " - $([Math]::Abs($b))" + "y"
        }
    }
    
    $equation += " = $c"
    return $equation
}

function Test-Answer {
    param($userX, $userY, $correctX, $correctY)
    
    return ($userX -eq $correctX) -and ($userY -eq $correctY)
}

function Get-UserInput {
    param($prompt)
    
    do {
        $input = Read-Host $prompt
        if ($input -match '^-?\d+$') {
            return [int]$input
        } else {
            Write-Host "Please enter a valid integer!" -ForegroundColor Red
        }
    } while ($true)
}

function Show-Congratulations {
    $messages = @(
        "🎉 Excellent work!",
        "🌟 Perfect! You're a math wizard!",
        "✅ Correct! Well done!",
        "💫 Amazing! You solved it!",
        "🔥 Fantastic job!"
    )
    $message = $messages | Get-Random
    Write-Host $message -ForegroundColor Green
}

function Show-Encouragement {
    $messages = @(
        "Don't give up! Try again.",
        "You can do it! Think carefully.",
        "Almost there! Check your calculations.",
        "Keep going! You'll get it."
    )
    $message = $messages | Get-Random
    Write-Host $message -ForegroundColor Yellow
}

# Main game loop
function Start-PuzzleGame {
    param($NumberOfPuzzles = 3)
    
    $score = 0
    $totalAttempts = 0
    $correctOnFirstTry = 0
    
    # Start timer
    $startTime = Get-Date
    
    Write-Host "`n=== Linear Equation Puzzle Challenge ===" -ForegroundColor Green
    Write-Host "Solve each system of equations for x and y" -ForegroundColor Yellow
    Write-Host "You have 3 attempts per puzzle. Good luck!`n" -ForegroundColor Yellow
    
    for ($puzzleNum = 1; $puzzleNum -le $NumberOfPuzzles; $puzzleNum++) {
        $system = Generate-LinearSystem
        $attempts = 0
        $solved = $false
        
        Write-Host "--- Puzzle $puzzleNum of $NumberOfPuzzles ---" -ForegroundColor Cyan
        Write-Host "Equation 1: $($system.Equation1)" -ForegroundColor White
        Write-Host "Equation 2: $($system.Equation2)" -ForegroundColor White
        Write-Host ""
        
        while ($attempts -lt 3 -and -not $solved) {
            $attempts++
            $totalAttempts++
            
            Write-Host "Attempt $attempts of 3" -ForegroundColor Gray
            $userX = Get-UserInput "Enter value for x"
            $userY = Get-UserInput "Enter value for y"
            
            if (Test-Answer -userX $userX -userY $userY -correctX $system.Solution.x -correctY $system.Solution.y) {
                Show-Congratulations
                $score += (4 - $attempts)  # 3 points for 1st try, 2 for 2nd, 1 for 3rd
                if ($attempts -eq 1) { $correctOnFirstTry++ }
                $solved = $true
            } else {
                if ($attempts -lt 3) {
                    Write-Host "❌ Incorrect. " -ForegroundColor Red -NoNewline
                    Show-Encouragement
                    Write-Host ""
                } else {
                    Write-Host "❌ Sorry, the correct answer was: x = $($system.Solution.x), y = $($system.Solution.y)" -ForegroundColor Red
                    Write-Host ""
                }
            }
        }
    }
    
    # Calculate time spent
    $endTime = Get-Date
    $timeSpent = $endTime - $startTime
    $minutes = [math]::Floor($timeSpent.TotalMinutes)
    $seconds = $timeSpent.Seconds
    
    # Calculate percentage score (max possible: 3 points per puzzle × number of puzzles)
    $maxScore = $NumberOfPuzzles * 3
    $percentage = [math]::Round(($score / $maxScore) * 100)
    
    # Display results
    Write-Host "=== Game Results ===" -ForegroundColor Green
    Write-Host "Time spent: $minutes minutes $seconds seconds" -ForegroundColor Cyan
    Write-Host "Puzzles solved: $NumberOfPuzzles" -ForegroundColor Cyan
    Write-Host "Correct on first try: $correctOnFirstTry/$NumberOfPuzzles" -ForegroundColor Cyan
    Write-Host "Total attempts: $totalAttempts" -ForegroundColor Cyan
    Write-Host "Raw score: $score/$maxScore" -ForegroundColor Cyan
    Write-Host "Final percentage: $percentage%" -ForegroundColor Cyan
    
    # Performance feedback
    Write-Host "`nPerformance: " -ForegroundColor Yellow -NoNewline
    if ($percentage -ge 90) {
        Write-Host "Outstanding! 🏆" -ForegroundColor Magenta
    } elseif ($percentage -ge 80) {
        Write-Host "Excellent! 🌟" -ForegroundColor Green
    } elseif ($percentage -ge 70) {
        Write-Host "Good job! 👍" -ForegroundColor Yellow
    } elseif ($percentage -ge 60) {
        Write-Host "Not bad! 💪" -ForegroundColor Blue
    } else {
        Write-Host "Keep practicing! 📚" -ForegroundColor Red
    }
}

# Game setup
Clear-Host
Write-Host "Welcome to the Linear Equation Puzzle Game!" -ForegroundColor Green
Write-Host "============================================`n"

do {
    $puzzleCount = Read-Host "How many puzzles would you like to solve? (1-10)"
    if ($puzzleCount -match '^(10|[1-9])$') {
        $NumberOfPuzzles = [int]$puzzleCount
        break
    } else {
        Write-Host "Please enter a number between 1 and 10!" -ForegroundColor Red
    }
} while ($true)

Write-Host "`nGet ready to start...`n"
Start-Sleep -Seconds 2

# Start the game
Start-PuzzleGame -NumberOfPuzzles $NumberOfPuzzles

# Play again option
Write-Host ""
$playAgain = Read-Host "Would you like to play again? (y/n)"
if ($playAgain -eq 'y' -or $playAgain -eq 'Y') {
    & $MyInvocation.MyCommand.Path
}
