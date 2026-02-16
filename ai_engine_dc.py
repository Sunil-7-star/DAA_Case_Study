WHITE="white"
BLACK="black"
class DivideConquerAI:
  def _find_best_move(self, candidates):
          if len(candidates) == 0:
              return None
          if len(candidates) == 1:
              return candidates[0]
  
          mid = len(candidates) // 2
          left = self._find_best_move(candidates[:mid])
          right = self._find_best_move(candidates[mid:])
  
          if left is None:
              return right
          if right is None:
              return left
  
          score_left = self.score(left[0], left[1])
          score_right = self.score(right[0], right[1])
          if score_left >= score_right:
              return left
          return right
