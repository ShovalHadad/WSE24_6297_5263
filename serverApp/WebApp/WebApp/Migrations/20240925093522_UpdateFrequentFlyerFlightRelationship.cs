using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WebApp.Migrations
{
    /// <inheritdoc />
    public partial class UpdateFrequentFlyerFlightRelationship : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Flights_FrequentFlyers_FlyerId",
                table: "Flights");

            migrationBuilder.RenameColumn(
                name: "FlyerId",
                table: "Flights",
                newName: "FrequentFlyerFlyerId");

            migrationBuilder.RenameIndex(
                name: "IX_Flights_FlyerId",
                table: "Flights",
                newName: "IX_Flights_FrequentFlyerFlyerId");

            migrationBuilder.AddForeignKey(
                name: "FK_Flights_FrequentFlyers_FrequentFlyerFlyerId",
                table: "Flights",
                column: "FrequentFlyerFlyerId",
                principalTable: "FrequentFlyers",
                principalColumn: "FlyerId",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Flights_FrequentFlyers_FrequentFlyerFlyerId",
                table: "Flights");

            migrationBuilder.RenameColumn(
                name: "FrequentFlyerFlyerId",
                table: "Flights",
                newName: "FlyerId");

            migrationBuilder.RenameIndex(
                name: "IX_Flights_FrequentFlyerFlyerId",
                table: "Flights",
                newName: "IX_Flights_FlyerId");

            migrationBuilder.AddForeignKey(
                name: "FK_Flights_FrequentFlyers_FlyerId",
                table: "Flights",
                column: "FlyerId",
                principalTable: "FrequentFlyers",
                principalColumn: "FlyerId",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
