
#include <map>
#include <vector>
#include <fstream>
#include <iostream>
#include <numeric>

enum Move {
    ROCK = 1,
    PAPER = 2,
    SCISSORS = 3
};

struct Round {
    Move whatOpponentWillPlay;
    Move whatIShouldPlay;
};
using Rounds = std::vector<Round>;

const std::map<char,Move> move = {
    { 'A', Move::ROCK },        { 'X', Move::ROCK },
    { 'B', Move::PAPER },       { 'Y', Move::PAPER },
    { 'C', Move::SCISSORS },    { 'Z', Move::SCISSORS },
};

Rounds readInputFile(const std::string& inputFilename) {
    std::vector<Round> rounds;

    std::ifstream file(inputFilename, std::ifstream::in);

    struct {char firstCharacter; char secondCharacter;} line;
    while (file >> line.firstCharacter >> line.secondCharacter) {
        Move whatOpponentWillPlay = move.at(line.firstCharacter);
        Move whatIShouldPlay = move.at(line.secondCharacter);
        Round round{whatOpponentWillPlay, whatIShouldPlay};

        rounds.push_back(round);
    }

    return rounds;
}



class GameInput {
    // 8 bits flag -- 4 bits for each move
    unsigned char val;

  public:
    GameInput(Move p1Move, Move p2Move) {
        this->val = (p1Move << 4) | p2Move;
    }

    operator unsigned char() const {
        return (unsigned char) this->val;
    }
};

enum Winner {
    P1,
    P2,
    none
};
using GameOutput = Winner;

const std::map<GameInput,GameOutput> rockPaperScissors = {
    { GameInput(Move::ROCK, Move::ROCK),            Winner::none },
    { GameInput(Move::ROCK, Move::PAPER),           Winner::P2 },
    { GameInput(Move::ROCK, Move::SCISSORS),        Winner::P1 },

    { GameInput(Move::PAPER, Move::ROCK),           Winner::P1 },
    { GameInput(Move::PAPER, Move::PAPER),          Winner::none },
    { GameInput(Move::PAPER, Move::SCISSORS),       Winner::P2 },

    { GameInput(Move::SCISSORS, Move::ROCK),        Winner::P2 },
    { GameInput(Move::SCISSORS, Move::PAPER),       Winner::P1 },
    { GameInput(Move::SCISSORS, Move::SCISSORS),    Winner::none },
};



enum Outcome {
    LOST = 0,
    DRAW = 3,
    WON = 6
};

const std::map<GameOutput,Outcome> outcome {
    { Winner::P1,       Outcome::WON },
    { Winner::none,     Outcome::DRAW },
    { Winner::P2,       Outcome::LOST }
};

int calculateScore(Round round) {
    auto gameInput = GameInput(round.whatIShouldPlay, round.whatOpponentWillPlay);
    GameOutput gameOutput = rockPaperScissors.at(gameInput);

    return round.whatIShouldPlay + outcome.at(gameOutput);
}

// g++ c.cpp
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