#include <map>

namespace rps {
    /* emulating extern enum values */
    using MoveEnum = int;
    namespace Move {
        extern MoveEnum ROCK;
        extern MoveEnum PAPER;
        extern MoveEnum SCISSORS;
    }

    class GameInput {
        // 8 bits flag -- 4 bits for each move
        unsigned char val;

      public:
        explicit GameInput(MoveEnum p1Move, MoveEnum p2Move);

        operator unsigned char() const;
    };

    enum Winner {
        P1,
        P2,
        none,
    };
    using GameOutput = Winner;
    using GameOutputEnum = GameOutput;

    const std::map<GameInput,GameOutputEnum> rockPaperScissors = {
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

    const std::map<MoveEnum,MoveEnum> losingMove = {
        { Move::ROCK,       Move::SCISSORS },
        { Move::PAPER,      Move::ROCK },
        { Move::SCISSORS,   Move::PAPER }
    };

    const std::map<MoveEnum,MoveEnum> winningMove = {
        { Move::ROCK,       Move::PAPER },
        { Move::PAPER,      Move::SCISSORS },
        { Move::SCISSORS,   Move::ROCK }
    };

}
