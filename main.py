from ai_jumper import geneticworld

# Genetic algorithm params
generationSize = 12
maxTravelLen = 15000
maxGenerationNum = 5000

# Run simulation
geneticworld.run(generationSize, maxTravelLen, maxGenerationNum)