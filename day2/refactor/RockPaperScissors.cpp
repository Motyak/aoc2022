#include <RockPaperScissors.h>

using namespace rps;

GameInput::GameInput(MoveEnum p1Move, MoveEnum p2Move) {
    this->val = (p1Move << 4) | p2Move;
}

GameInput::operator unsigned char() const {
    return this->val;
}
