from ai_jumper import geneticworld

# Genetic algorithm params
generationSize = 10
bestJumpersNum = 3
mutantsJumpersNum = 4
maxTravelLen = 10000
maxGenerationNum = 5000

# Run simulation
geneticworld.run(generationSize, bestJumpersNum, mutantsJumpersNum, maxTravelLen, maxGenerationNum)