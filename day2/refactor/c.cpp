#include <RockPaperScissors.h>

#include <map>
#include <vector>
#include <fstream>
#include <iostream>
#include <numeric>
#include <variant>

/* override values for enum rps::Move::xx */
rps::MoveEnum rps::Move::ROCK = 1;
rps::MoveEnum rps::Move::PAPER = 2;
rps::MoveEnum rps::Move::SCISSORS = 3;

enum Outcome {
    LOST = 0,
    DRAW = 3,
    WON = 6,
};
using OutcomeEnum = Outcome;

struct Round {
    rps::MoveEnum whatOpponentWillPlay;
    OutcomeEnum requiredOutcome;
};
using RoundEnum = Round;
using Rounds = std::vector<RoundEnum>;

const std::map<char,rps::MoveEnum> move = {
    { 'A', rps::Move::ROCK },    
    { 'B', rps::Move::PAPER },   
    { 'C', rps::Move::SCISSORS },
};

using EitherGameOutputOrChar = std::variant<rps::GameOutput,char>;
const std::map<EitherGameOutputOrChar,OutcomeEnum> outcome {
    { rps::Winner::P1,      Outcome::WON },
    { 'Z',                  Outcome::WON },

    { rps::Winner::none,    Outcome::DRAW },
    { 'Y',                  Outcome::DRAW },

    { rps::Winner::P2,      Outcome::LOST },
    { 'X',                  Outcome::LOST }
};

Rounds readInputFile(const std::string& inputFilename) {
    std::vector<RoundEnum> rounds;

    std::ifstream file(inputFilename, std::ifstream::in);

    struct {char firstCharacter; char secondCharacter;} line;
    while (file >> line.firstCharacter >> line.secondCharacter) {
        rps::MoveEnum whatOpponentWillPlay = move.at(line.firstCharacter);
        OutcomeEnum requiredOutcome = outcome.at(line.secondCharacter);
        RoundEnum round{whatOpponentWillPlay, requiredOutcome};

        rounds.push_back(round);
    }

    return rounds;
}

rps::MoveEnum getMoveMatchingRequiredOutcome(RoundEnum round) {
    switch (round.requiredOutcome) {
        case Outcome::DRAW:
            return round.whatOpponentWillPlay;

        case Outcome::WON:
            return rps::winningMove.at(round.whatOpponentWillPlay);

        case Outcome::LOST:
            return rps::losingMove.at(round.whatOpponentWillPlay);
    };
}

int calculateScore(RoundEnum round) {
    rps::MoveEnum whatIShouldPlay = getMoveMatchingRequiredOutcome(round);
    auto gameInput = rps::GameInput(whatIShouldPlay, round.whatOpponentWillPlay);
    rps::GameOutput gameOutput = rps::rockPaperScissors.at(gameInput);

    return whatIShouldPlay + outcome.at(gameOutput);
}

// g++ RockPaperScissors.cpp c.cpp --std=c++17 -I .
int main()
{
    const std::string INPUT_FILE = "input.txt";

    Rounds rounds = readInputFile(INPUT_FILE);
    
    int res = std::accumulate(
        rounds.begin(),
        rounds.end(),
        0,
        [](int sum, const auto& round) { return sum + calculateScore(round); }
    );

    std::cout << res << std::endl;
}
