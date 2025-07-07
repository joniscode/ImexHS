

export interface StainCalculation {
  id: string;
  imageName: string;
  width: number;
  height: number;
  totalPoints: number;
  pointsInside: number;
  estimatedArea: number;
  timestamp: string | Date;
}