
#include <map>
#include <vector>
#include <fstream>
#include <iostream>
#include <numeric>
#include <variant>

enum Outcome {
    LOST = 0,
    DRAW = 3,
    WON = 6
};

enum Move {
    ROCK = 1,
    PAPER = 2,
    SCISSORS = 3
};

struct Round {
    Move whatOpponentWillPlay;
    Outcome requiredOutcome;
};
using Rounds = std::vector<Round>;

const std::map<char,Move> move = {
    { 'A', Move::ROCK },    
    { 'B', Move::PAPER },   
    { 'C', Move::SCISSORS },
};

enum Winner {
    P1,
    P2,
    none
};
using GameOutput = Winner;

using EitherGameOutputOrChat = std::variant<GameOutput,char>;
const std::map<EitherGameOutputOrChat,Outcome> outcome {
    { Winner::P1,       Outcome::WON },
    { 'Z',              Outcome::WON },

    { Winner::none,     Outcome::DRAW },
    { 'Y',              Outcome::DRAW },

    { Winner::P2,       Outcome::LOST },
    { 'X',              Outcome::LOST }
};

Rounds readInputFile(const std::string& inputFilename) {
    std::vector<Round> rounds;

    std::ifstream file(inputFilename, std::ifstream::in);

    struct {char firstCharacter; char secondCharacter;} line;
    while (file >> line.firstCharacter >> line.secondCharacter) {
        Move whatOpponentWillPlay = move.at(line.firstCharacter);
        Outcome requiredOutcome = outcome.at(line.secondCharacter);
        Round round{whatOpponentWillPlay, requiredOutcome};

        rounds.push_back(round);
    }

    return rounds;
}



class GameInput {
    // 8 bits flag -- 4 bits for each move
    unsigned char val;

  public:
    explicit GameInput(Move p1Move, Move p2Move) {
        this->val = (p1Move << 4) | p2Move;
    }

    operator unsigned char() const {
        return this->val;
    }
};

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

const std::map<Move,Move> losingMove = {
    { Move::ROCK,       Move::SCISSORS },
    { Move::PAPER,      Move::ROCK },
    { Move::SCISSORS,   Move::PAPER }
};

const std::map<Move,Move> winningMove = {
    { Move::ROCK,       Move::PAPER },
    { Move::PAPER,      Move::SCISSORS },
    { Move::SCISSORS,   Move::ROCK }
};



Move getMoveMatchingRequiredOutcome(Round round) {
    switch (round.requiredOutcome) {
        case Outcome::DRAW:
            return round.whatOpponentWillPlay;

        case Outcome::WON:
            return winningMove.at(round.whatOpponentWillPlay);

        case Outcome::LOST:
            return losingMove.at(round.whatOpponentWillPlay);
    };
}

int calculateScore(Round round) {
    Move whatIShouldPlay = getMoveMatchingRequiredOutcome(round);
    auto gameInput = GameInput(whatIShouldPlay, round.whatOpponentWillPlay);
    GameOutput gameOutput = rockPaperScissors.at(gameInput);

    return whatIShouldPlay + outcome.at(gameOutput);
}

// g++ c.cpp --std=c++17
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